from flask import g, request
from flask_httpauth import HTTPBasicAuth

from backend.app.models.user import User as MyUser

auth = HTTPBasicAuth()

def check_password(username_or_token, password):
    # first try to authenticate by token
    print (' XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ')
    if 'X-API-KEY' in request.headers:
        username_or_token = request.headers['X-API-KEY']

    user = MyUser.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = MyUser.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


'''
    # CODE FRIEDHOF

    def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if token != 'mytoken':
            return {'message' : 'Your token is wrong, wrong, wrong!!!'}, 401

        print('TOKEN: {}'.format(token))

        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = User.query.filter_by(username = username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
    
        return f(*args, **kwargs)

    return decorated

'''    