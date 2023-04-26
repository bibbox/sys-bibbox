from flask import jsonify
from backend.app import app, db, restapi
from flask_restplus import Namespace, Resource


api = Namespace('kc', description='KeyCloak Ressources')
restapi.add_namespace (api, '/kc')

"""
Here we define the routes for the KeyCloak Admin API for managing Users

User Handling Routes:
    Get Users
    
    Create User
    Delete User
    Update User
    
    Set Roles for User (add, remove)
        - bibbox-admin
        - bibbox-standard

    Set Groups for User (add, remove)
        - sys-bibbox-admin-group
        - sys-bibbox-default-group
        - sys-bibbox-demo-group
"""

@api.route('/ping')
@api.doc("Just to test if the KeyCloak API is alive")
class Ping(Resource):
    def get(self):
        return {"reply":"PONG"}
