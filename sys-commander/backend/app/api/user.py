# -*- coding: utf-8 -*-
"""User Route for Demo application."""

from flask import Blueprint
from flask import jsonify

from backend.app.services.user_service import UserService
from backend.app.api import api

user_service = UserService()

@api.route("/users")
def  get_users():
    users = user_service.all()
    return users

@api.route("/user/<int:id>")
def get_user(id):
    print ("looking for user with id = ", id)
    user = user_service.get(id)
    return jsonify (user.as_dict())
