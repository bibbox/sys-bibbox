# -*- coding: utf-8 -*-
"""Default api blueprints for Demo application."""

'''
from flask import jsonify
from backend.app import app, db, restapi

@restapi.route("/")
def hello():
    return "Hello from Flask using Python 3.6.2!!"

@restapi.route("/ping")
def ping():
    return jsonify({"status": 200, "msg":"Hallo Heimo -  message is coming from Flask backend!"})
'''
from flask_restx import Namespace, Api, Resource, fields
from backend.app import app, db, restapi
api = Namespace('info', description='Information')
restapi.add_namespace (api, '/info')
@api.route('/ping')
@api.doc("Ping BIBBOX backend")
class Ping(Resource):
    def get(self):
        return {"msg": "Hello - This message is coming from BIBBOX backend!"}, 200


