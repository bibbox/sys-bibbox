# -*- coding: utf-8 -*-
"""User Route for App Catalogues"""

import os
import json
from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Api, Resource, fields, reqparse

from backend.app import app, db, restapi
from backend.app.services.keycloak_service import auth_token_required
from backend.app.services.keyvalue_service import KeyValueService
from backend.app.services.keycloak_service import KeycloakRoles
from backend.app.models.keyvalue import KeyValue
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exc

keyvalue_service = KeyValueService()

api = Namespace('keyvalue', description='KeyValue Ressources')
restapi.add_namespace (api, '/keyvalue')

keyvaluemodel = api.model('Model', {
    'id' : fields.String,
    'keys': fields.String,
    'values' :  fields.String
})

@api.route("/<string:key>")
@api.doc(params={'key': 'key'})
class KeyValues(Resource):

    @api.doc("Get value for key")
    @auth_token_required()
    def get (self, key):
        #print ("looking for value with key = ", key)
        keyvalue = keyvalue_service.get_value_by_key(key)
        #print(keyvalue)
        if keyvalue is None:
            return None,204
        return jsonify(keyvalue.as_dict())

    @api.doc("Create a key value pair")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def post (self, key):
        try:
            # Check if 'keys' and 'value' are present in the JSON request
            keyvalue_descr = request.json
            keys = str(key)
            value = keyvalue_descr.get('value')

            if not keys or not value:
                return {'error': 'Missing keys or value in the request'}, 400

            # Create and add a new KeyValue object to the database
            new_key_value = KeyValue(keys, value)
            db.session.add(new_key_value)
            print("123")

            try:
                db.session.commit()

            except IntegrityError as e:
                # Handle the database integrity error (e.g., unique constraint violation)
                db.session.rollback()  # Rollback the transaction
                return {'error': 'Resource with the same key already exists'}, 409

            # Assuming self.get returns a response object
            res = self.get(keys)
            # Check if the status code is 200 and change it to 201
            if res.status_code == 200:
                res.status_code = 201
            return res
        except Exception as e:
            # Handle any exceptions that may occur during the process
            return {'error': str(e)}, 500

    @api.doc("Update a key value pair")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def put(self, key):
        try:
            # Check if 'keys' and 'value' are present in the JSON request
            keyvalue_descr = request.json
            keys = str(key)
            value = keyvalue_descr.get('value')

            if not keys or not value:
                return {'error': 'Missing keys or value in the request'}, 400

            # Check if the resource with the specified key exists
            existing_key_value = keyvalue_service.get_value_by_key(keys)

            if not existing_key_value:
                return {'error': 'Resource not found'}, 404

            # Update the value for the existing resource
            existing_key_value.values = value
            print (existing_key_value)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()  # Rollback the transaction
                return {'error': 'Resource with the same key already exists'}, 409

            # Return a success response
            return {'message': 'Resource updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @api.doc("Delete a key value pair")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def delete(self, key):
        try:
            keys = str(key)

            # Check if the resource with the specified key exists
            existing_key_value = KeyValue.query.filter_by(keys=keys).first()

            if not existing_key_value:
                return {'error': 'Resource not found'}, 404

            # Delete the resource
            db.session.delete(existing_key_value)
            db.session.commit()

            # Return a success response
            return {'message': 'Resource deleted successfully'}, 204
        except Exception as e:
            return {'error': str(e)}, 500
