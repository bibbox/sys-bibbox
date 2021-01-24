# -*- coding: utf-8 -*-
"""User Route for Demo application."""

from flask import Blueprint, g, abort, request, jsonify,  url_for
from flask_httpauth import HTTPBasicAuth

from backend.app import db
from backend.app.models.user import User
from backend.app.services.user_service import UserService
from backend.app.api import api

user_service = UserService()
auth = HTTPBasicAuth()

@api.route("/users")
def  get_users():
    users = user_service.all()
    return users

@api.route('/users', methods = ['POST'])
def new_user():
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

@api.route("/user/<int:id>")
def get_user(id):
    print ("looking for user with id = ", id)
    user = user_service.get(id)
    return jsonify (user.as_dict())

@api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

# curl -u heimo:vendetta -i -X GET http://127.0.0.1:20080/api/v1/token

@api.route('/secrets')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

# curl -u heimo:vendetta -i -X GET http://127.0.0.1:20080/api/v1/secrets
# curl -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxMTUyOTExMSwiZXhwIjoxNjExNTI5NzExfQ.eyJpZCI6OH0.0aC4d1w_QUrAr87CmN3n8mWCcAV36goUi2SlI8r70nXjjXj_KzzZVsfG4Uta5iYk1YHWJ8XmH2INtnFqz3mWpA:xxx -i -X GET http://127.0.0.1:20080/api/v1/secrets


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True