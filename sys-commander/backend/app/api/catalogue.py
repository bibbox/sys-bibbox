# -*- coding: utf-8 -*-
"""User Route for Catalogues"""

from flask import Blueprint, request, jsonify
from flask_restplus import Api, Resource, fields

from backend.app.api import api
from backend.app import db
from backend.app.models.catalogue import Catalogue
from backend.app.services.catalogue_service import CatalogueService


catalogue_service = CatalogueService()

from backend.app.bibbox.app_catalogue  import AppCatalogue

appCatalogue = AppCatalogue ()

# take finaly this approach (doc out of code) 
# https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f 

@api.route("/catalogues")
def  get_catalogues ():
    cat = appCatalogue.availableCatalogues ()
    return jsonify(cat)

@api.route("/catalogues/active", methods = ['POST', 'GET'])
def  get_active_catalogue ():
    if request.method == 'POST':
       pass
    else:
       activeCatalogueName = appCatalogue.activeCatalogue ()    
    return jsonify(activeCatalogueName)

@api.route("/apps")
def  get_full_app_descriptions_from_active_catalogue ():
    activeCatalogeName = appCatalogue.activeCatalogue ()   
    apps = appCatalogue.appDescriptions (activeCatalogeName)
    return jsonify(apps)

@api.route("/app_names")
def  get_app_names_from_active_catalogue ():
    activeCatalogeName = appCatalogue.activeCatalogue ()   
    appnames = appCatalogue.appNames (activeCatalogeName)
    return jsonify(appnames)
