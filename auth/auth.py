import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import requests
import sys
import os 


# Configurations gotten from the account created on Auth0
AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
JWT_TOKEN_ENCRYPTION_ALGORITHMS, = os.environ["JWT_TOKEN_ENCRYPTION_ALGORITHMS"]
AUTH0_JWT_API_AUDIENCE = os.environ["AUTH0_JWT_API_AUDIENCE"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CALLBACK_URL = os.environ["AUTH0_CALLBACK_URL"]

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def validate_auth_header(auth_header):
    splitted_header = auth_header.split()
    bearer_part = splitted_header[0]
    valid_auth = True
    if len(splitted_header) != 2:
        valid_auth = False
    if bearer_part.lower() != "bearer":
        valid_auth = False
    return valid_auth


def get_token():
    headers = request.headers
    if 'Authorization' in request.headers:
        auth_header = headers['Authorization']
        valid_header = validate_auth_header(auth_header)
        if not valid_header:
            print("INVALID")
            raise AuthError({
                'status': 401,
                'message': 'Unauthorized'
            }, status_code=401)
        token = auth_header.split()[1]
        return token
    raise AuthError({
        'status': 401,
        'message': 'Unauthorized'
    }, status_code=401)


def verify_decode_jwt(token):
    try:
        jwt_unverified_headers = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({
            'status': 401,
            'message': 'invalid jwt token'
        }, status_code=401)
    public_keys_url = f' https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    response = requests.get(public_keys_url)
    jwks = response.json() if response.status_code == 200 else None
    if 'kid' not in jwt_unverified_headers:
        raise AuthError({
            'status': 401,
            'message': 'invalid jwt token'
        }, status_code=401)
    if jwks:
        matched_key = {}
        if 'keys' in jwks:
            for key in jwks['keys']:
                if key['kid'] == jwt_unverified_headers['kid']:
                    matched_key = key
        if matched_key:
            try:
                issuer = f'https://{AUTH0_DOMAIN}/'
                decoded_jwt = jwt.decode(
                    token,
                    matched_key,
                    algorithms=JWT_TOKEN_ENCRYPTION_ALGORITHMS,
                    audience=AUTH0_JWT_API_AUDIENCE,
                    issuer=issuer
                )
                return decoded_jwt
            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'status': 401,
                    'message': 'token has expired'
                }, status_code=401)
            except jwt.JWTClaimsError:
                raise AuthError({
                    'status': 401,
                    'message': 'invalid claim in jwt token'
                }, status_code=401)
            except jwt.JWTError:
                raise AuthError({
                    'status': 401,
                    'message': 'invalid signature'
                }, status_code=401)
            except Exception:
                print(sys.exc_info())
                raise AuthError({
                    'status': 401,
                    'message': 'invalid auth token'
                }, status_code=401)
            except Exception:
                print(sys.exc_info())
                raise AuthError({
                    'status': 500,
                    'message': 'token has expired'
                }, status_code=500)
        raise AuthError({
            'code': 'invalid token',
            'description': 'please provide a valid token.'
        }, 401)
    raise AuthError({
        'code': 'invalid token',
        'description': 'please provide a valid token.'
    }, 401)



def check_permissions(permission, jwt_payload):
    jwt_has_permissions = 'permissions' in jwt_payload
    if not jwt_has_permissions or (jwt_has_permissions and permission not in jwt_payload['permissions']):
        raise AuthError({
            'code': 'unauthorized',
            'description': 'you dnn\'t have permissions to view this resource .'
        }, 401)
    return True


def auth_required(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token()
            jwt_payload = verify_decode_jwt(token)
            check_permissions(permission, jwt_payload)
            return f(jwt_payload, **kwargs)
        return wrapper
    return requires_auth_decorator