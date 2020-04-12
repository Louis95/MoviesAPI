
from flask import Flask
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from models import set_up_db
from models import Movies, Actors, Sets, db
import sys
from auth.auth import AuthError, auth_required 

MAX_MOVIES_PER_PAGE = 10
MAX_ACTORS_PER_PAGE = 10


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
@auth_required('get:movies')
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
@auth_required('post:movies')
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
@auth_required('patch:movies')
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
@auth_required('delete:movies')
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
@auth_required('get:actors')
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
@auth_required('get:actor-details')
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
@auth_required('post:actors')
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
@auth_required('delete:actors')
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
@auth_required('patch:actors')
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