# -*- coding: utf-8 -*-
"""User Route for Demo application."""

from flask import Blueprint, g, abort, request, jsonify,  url_for
from flask_restplus import Namespace, Api, Resource, fields
from flask_httpauth import HTTPBasicAuth
from functools import wraps 

from backend.app import app, db, restapi
from backend.app.api.authentication import check_password

from backend.app.services.user_service import UserService

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

authorization = {
    'apikey': {
        'type': 'apiKey',
        'in':   'header',
        'name': 'X-API-KEY'
    },
    'basic': {
        'type': 'basic',
    }
}

api = Namespace('users', 
                description='Users',     
                security='apiKey',
                authorizations = authorization)

restapi.add_namespace (api, '/users')

user_service = UserService()
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    return check_password (username_or_token, password)

@api.route("/")
class Users(Resource):
      
    @api.doc(security='apikey')   
    @api.doc(responses={200: 'sucess'})
    @auth.login_required
    def get(self):
        users = user_service.all_as_dict()
        for u in users:
            del u['password_hash']
        return  jsonify(users)

    @api.doc(responses={403: 'Not Authorized'})
    @api.doc(responses={ 202: 'Accepted', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params= { 'username': 'name', 'password': 'userspassword' })
    @auth.login_required
    def post():
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400) # missing arguments
        if User.query.filter_by(username = username).first() is not None:
            abort(400) # existing user
        user = User(username = username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({ 'username': user.username }), 201, {'Location': url_for('api.get_user', id = user.id, _external = True)}

# curl -i -X POST -H "Content-Type: application/json" -d '{"username":"heimo","password":"vendetta"}' http://127.0.0.1:20080/api/v1/users

@api.route("/<int:id>")
@api.doc(params={'id': 'user id'})
class User(Resource):

    def get (self):
        print ("looking for user with id = ", id)
        user = user_service.get(id)
        return jsonify (user.as_dict())

@api.doc(security='basic')   
@api.route("/token")
class GetAuthToken(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600})

@api.doc(security='apikey')  
@api.route('/secrets')
class Sectrets(Resource):
    @auth.login_required
    def get(self):
        return {'message' : 'Token works'}, 200

# curl -u v:vendetta -i -X GET http://127.0.0.1:5010/api/v1/users/token



