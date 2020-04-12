
from flask import Flask
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from models import set_up_db
from models import Movies, Actors, Sets, db
import sys


MAX_MOVIES_PER_PAGE = 10
MAX_ACTORS_PER_PAGE = 10





import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
# Configurations gotten from the account created on Auth0
AUTH0_DOMAIN = 'serverless-todo-app.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


"""
This function will get the authentification header
        
        :return: token
"""
def get_token_auth_header():
    """Will enable them to gain an access from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


"""
This function will check the permissions of each user perculiar to its role.
        :param permission: the permission
        :param payload: part of response
        :return: 
"""

def check_permissions(permission, payload):
    if 'permissions' not in payload:
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True




"""
 Verify the decoded jwt tokens.
        :param token: token to be verified
        
        :return: nothing
"""

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Now let's finally verify
    if rsa_key:
        try:
            # We'll use our key to validate the JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'wrong claims.Please, check the audience'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
 Implementation of the requirement authentification this decorator will be
 place before each request to check that the permission is satisfied
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator





















def create_app(test_config=None):
    # create and configure the app
    flask_app = Flask(__name__)
    set_up_db(flask_app)
    CORS(flask_app)
    return flask_app


app = create_app()



def paginate(items, max_per_page):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * max_per_page
    end = start + max_per_page
    return items[start:end]

@app.route("/movies", methods=["GET"])
def get_movies(token):
    movies_query = Movies.query.all()
    movies_list = list(map(Movies.show, movies_query))
    paginated_list = paginate(movies_list, MAX_MOVIES_PER_PAGE)
    return jsonify({
        'movies': paginated_list,
        'total_count': len(movies_list),
        'success': True
    })

@app.route("/movies", methods=["POST"])
def post_movie(token):
    post_data = request.get_json()
    if 'title' in post_data and 'release_date' in post_data:
        try:
            new_movie = Movies(title=post_data['title'],
                               release_date=post_data['release_date'])
            if 'actors' in post_data:
                actors_list = post_data['actors']
                for actor in actors_list:
                    actor_id = actor['id']
                    actor_data = Actors.query.get(actor_id)
                    if actor_data:
                        movie_set = Sets(movie_id=new_movie.id,
                                         actor_id=actor_id)
                        movie_set.insert()

            new_movie.insert()
            return jsonify({
                'id': new_movie.id,
                'success': True
            })
        except SQLAlchemyError:
            print(sys.exc_info())
            db.session.rollback()
            abort(400)
    abort(400)


@app.route("/movies/<int:movie_id>", methods=["PATCH"])
def patch_movie(token, movie_id):
    movie = Movies.query.get(movie_id)
    if not movie:
        abort(404)
    if request.method == 'PATCH':
        post_data = request.get_json()
        if 'title' in post_data:
            movie.title = post_data.get('title')
        if 'release_date' in post_data:
            movie.release_date = post_data.get('release_date')
        if 'actors' in post_data:
            actors_list = post_data['actors']  # list of actors for this movie
            for actor_id in actors_list:
                actor_data = Actors.query.get(actor_id)
                if actor_data:
                    movie_set = Sets(movie_id=movie.id, actor_id=actor_id)
                    movie_set.insert()
        try:
            movie.update()
            return jsonify({
                'id': movie.id,
                'success': True
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(400)


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(token, movie_id):
    movie = Movies.query.get(movie_id)
    if not movie:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            'id': movie_id,
            'success': True
        })
    except SQLAlchemyError:
        db.session.rollback()
        abort(400)

@app.route("/actors", methods=["GET"])
def get_actors(token):
    actors_query = Actors.query.all()
    actors_list = list(map(Actors.show, actors_query))
    paginated_list = paginate(actors_list, MAX_ACTORS_PER_PAGE)
    return jsonify({
        'actors': paginated_list,
        'total_count': len(paginated_list),
        'success': True
    })

@app.route("/actors/<int:actor_id>", methods=["GET"])
def show_actor(token, actor_id):
    actor_query = Actors.query.get(actor_id).show()
    if not actor_query:
        abort(404)
    movies_featured = [movie_set.movie_id for movie_set in
                       Sets.query.options(db.joinedload(Sets.actors))
                           .filter(Sets.actor_id == actor_id).all()]
    return jsonify({
        'actor': actor_query,
        'movies_featured_in': len(movies_featured)
    })

@app.route("/actors", methods=["POST"])
def post_actor(token):
    post_data = request.get_json()
    if 'name' in post_data and 'age' in post_data and 'gender' in post_data:
        new_actor = Actors(name=post_data['name'],
                           age=post_data['age'], gender=post_data['gender'])
        try:
            new_actor.insert()
            return jsonify({
                'id': new_actor.id,
                'success': True
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(400)
    abort(400)

@app.route("/actors/<int:actor_id>", methods=["DELETE"])
def delete_actors(token, actor_id):
    actor = Actors.query.get(actor_id)
    if not actor:
        abort(404)
    try:
        actor.delete()
        return jsonify({
            'id': actor_id,
            'success': True
        })
    except SQLAlchemyError:
        db.session.rollback()
        abort(400)

@app.route("/actors/<int:actor_id>", methods=["PATCH"])
def patch_actor(token, actor_id):
    actor = Actors.query.get(actor_id)
    if not actor:
        abort(404)
    data = request.get_json()
    if 'name' in data:
        actor.name = data['name']
    if 'age' in data:
        actor.age = data['age']
    if 'gender' in data:
        actor.gender = data['gender']
    try:
        actor.update()
        return jsonify({
            "id": actor_id,
            "success": True
        })
    except SQLAlchemyError:
        db.session.rollback()
        abort(400)


#You need to use following line [app Flask(__name__]
# app = Flask(__name__)
# @app.route('/')
# def index():
#     return "Hello World with flask"


if __name__ == '__main__':
    app.run(port=5000,debug=True)