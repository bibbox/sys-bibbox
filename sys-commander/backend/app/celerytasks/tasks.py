import os
import time
import random
import logging
import requests
import simplejson

from flask import current_app, render_template
from backend.app import app_celerey
from backend.app import db

from backend.app.models.catalogue import Catalogue
from backend.app.services.catalogue_service import CatalogueService

from celery.task.control import inspect
from celery_singleton import Singleton

catalogue_service = CatalogueService()


@app_celerey.task(bind=True, base=Singleton, name='tasks.syncAppCatalogue')
def syncAppCatalogue (self, catalogueNames):
    
    cataloguesInDB = catalogue_service.all_as_dict()
    catalogueNames_ID = {}
    for ce in cataloguesInDB:
        catalogueNames_ID[ce['name']] = ce['id']

    print (catalogueNames_ID)
    for cn in catalogueNames:
        url = 'https://raw.githubusercontent.com/bibbox/application-store/master/' + cn + '.json'
        try:
            download = requests.get(url).content
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
        try:
            # so we know that the json is valid
            params = simplejson.loads(download)
        except Exception:
#            bibbox_logger.exception('Error while loading eB3Kit.json file: ', exc_info=True)
            raise Exception('Error while loading catalogue file')
        
        contentAsJson = simplejson.dumps(params)
        if cn in catalogueNames_ID.keys():    
            ce = catalogue_service.get (catalogueNames_ID[cn])
            ce.content = contentAsJson
            db.session.commit()
        else: 
            ce = Catalogue(name=cn, content= contentAsJson)
            db.session.add(ce)
            db.session.commit()


