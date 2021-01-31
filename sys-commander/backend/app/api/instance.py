from flask import Flask
from flask_restplus import Namespace, Api, Resource, fields
from backend.app import app, db, restapi


api = Namespace('instances', description='Instance Ressources')
restapi.add_namespace (api, '/instances')

@api.route('/ping')
class Ping(Resource):
    def get(self):
        return {"reply":"PONG"}


@api.route('/<id>')
@api.doc(params={'id': 'An ID'})
class Instance(Resource):
    def get(self):
        return {"kuck kuck"}

    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)