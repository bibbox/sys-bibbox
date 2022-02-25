import os
import time
import random
import logging
import requests
import simplejson

from flask import current_app
from backend.app import app_celerey
from backend.app import db

from backend.app.models.catalogue import Catalogue
from backend.app.services.catalogue_service import CatalogueService

from backend.app.models.app import BibboxApp
from backend.app.services.app_service import AppService

#from celery.task.control import inspect
from celery_singleton import Singleton

catalogue_service = CatalogueService()
app_service = AppService()

def githubprefix (github_organization, appid, version):
    # if version == 'development':
    if version == 'latest':
        return "https://github.com/" + github_organization +  "/" + appid + "/"
    else: 
        return "https://github.com/" + github_organization +  "/" + appid + "/tree/" + version + "/"

def rawgithubprefix (github_organization, appid, version):
    # if version == 'development':
    if version == 'latest':
        return "https://raw.githubusercontent.com/" + github_organization +  "/" + appid + "/master/"
    else: 
        return "https://raw.githubusercontent.com/" + github_organization +  "/" + appid + "/" + version + "/"

def loadAndCheckJsonFromGit (url):
    #print ("read info from - ", url)
    try:
        response = requests.get(url)
        #print (download)
    except Exception as e:
        raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection! Error: ' + str(e))

    download = response.content
    if response.status_code != 200:
        raise Exception('An error has occurred: '+download)


    try:
        json_as_dict = simplejson.loads(download)
    except Exception:
       raise Exception('Report a miss configured JSON')
    json_again = simplejson.dumps(json_as_dict)  
    return json_again
    

@app_celerey.task(bind=True, name='tasks.syncAppCatalogue', base=Singleton, lock_expiry=60) # without singleton, we get recurring queuePool size overflow errors
def syncAppCatalogue (self, catalogueNames):
    
    cataloguesInDB = catalogue_service.all_as_dict()
    catalogueNames_ID = {}
    for ce in cataloguesInDB:
        catalogueNames_ID[ce['name']] = ce['id']
    print('Synching App Catalogue')
    # print (catalogueNames_ID)
    for cn in catalogueNames:
        url = 'https://raw.githubusercontent.com/bibbox/application-store/master/' + cn + '.json'
        contentAsJson = loadAndCheckJsonFromGit (url)
        if cn in catalogueNames_ID.keys():    
            ce = catalogue_service.get (catalogueNames_ID[cn])
            ce.content = contentAsJson
            db.session.commit()
        else: 
            ce = Catalogue(name=cn, content= contentAsJson)
            db.session.add(ce)
            db.session.commit()
    
    appVersions= {}
    for cn in catalogueNames:
      c = catalogue_service.catalogue (cn)
      if c:
          apps = simplejson.loads(c.content)  
          for app_groups in apps:
            for group_member in app_groups ['group_members']:
                app_name =  group_member ['app_name']
                for version in group_member ['versions']:
                    if app_name in  appVersions:
                        if version['app_version'] not in appVersions[app_name]:
                            appVersions [app_name].append (version['app_version'])
                    else:
                        appVersions [app_name] = [version['app_version']]
                        
    for appid in appVersions.keys():
        appinfo = ""
        envparam = ""
        for v in appVersions[appid]:
            appinfo_url = rawgithubprefix ('bibbox', appid, v) + "appinfo.json"
            envp_url    = rawgithubprefix ('bibbox', appid, v) +  "environment-parameters.json" 
        try:
            appinfo = loadAndCheckJsonFromGit (appinfo_url)
            envparam = loadAndCheckJsonFromGit (envp_url)
        except Exception:
            print ("Metadata incorrect for ", appid, " ", v)  

        v_rec = app_service.version (appid, v)
        if v_rec:
            v_rec.appinfo = appinfo
            v_rec.environment_parameters = envparam
            db.session.commit()     
        else:
            v_rec= BibboxApp (appid, v, appinfo, envparam)
            db.session.add(v_rec)
            db.session.commit()        
    print('Synching App Catalogue completed')
    
