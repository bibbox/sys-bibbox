# -*- coding: utf-8 -*-
"""User Route for App Catalogues"""

from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Api, Resource, fields, reqparse

from backend.app import app, db, restapi
from backend.app.bibbox.app  import AppCatalogue
from backend.app.models.app import BibboxApp
from backend.app.models.catalogue import Catalogue
from backend.app.services.catalogue_service import CatalogueService

catalogue_service = CatalogueService()
appCatalogue = AppCatalogue ()

# take finaly this approach (doc out of code) 
# https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f 


api = Namespace('apps', description='Catalogue Ressources')
restapi.add_namespace (api, '/apps')


installparameter = api.model('InstallParameter', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


@api.route("/catalogues")
class Catalogues(Resource):
    def get(self):
        cat = appCatalogue.availableCatalogues ()
        return cat

@api.route("/catalogues/active")
class ActiveCatalogue(Resource):
    def get(self):
        return appCatalogue.activeCatalogue ()  

@api.route("/")
class AppsInActiveCataloge(Resource):
    def get(self):
        activeCatalogeName = appCatalogue.activeCatalogue ()   
        apps = appCatalogue.appDescriptions (activeCatalogeName)
        return apps

#http://127.0.0.1:5010/api/v1/apps/envparameter?appid=app-xnat&version=development
@api.param('version', 'version')
@api.param('appid', 'app id')
@api.route("/envparameter")
class InstallParameter(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('version')
        parser.add_argument('appid')
        args = parser.parse_args()
        version = args['version']
        appid = args['appid']
        envpar = appCatalogue.environment_parameters (appid, version)   
        return envpar

@api.param('version', 'version')
@api.param('appid', 'app id')
@api.route("/info")
class AppInfo (Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('version')
        parser.add_argument('appid')
        args = parser.parse_args()
        version = args['version']
        appid = args['appid']
        appinfo = appCatalogue.appInfo (appid, version)   
        return appinfo
# demo
# http://127.0.0.1:5010/api/v1/apps/info?appid=app-redcap&version=development



#@api.param('testparam', 'test')
@api.doc(

)
@api.route("/test", doc={"description": 'testdescription for the endpoint'})
class TestClass (Resource):
    @api.doc(
        'get test stuff',     
        responses={
            200: 'Success',
            400: 'Validation Error',
            418: "I'm a teapot"
        },
        params={
            "testparam": "a Testparam"
        }
    )
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('testparam')
        args = parser.parse_args()
        tp = args['testparam']
        return {1: dir(api.doc())}