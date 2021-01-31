import os
import time
import random
import logging
import requests
import simplejson

from flask import current_app, render_template

from backend.app.models.catalogue import Catalogue
from backend.app.services.catalogue_service import CatalogueService

from backend.app.models.app import BibboxApp
from backend.app.services.app_service import AppService

from backend.app import create_app
app = create_app("developmentlocal")
from backend.app import  db
print ("SQLALCHEMY_DATABASE_URI =", app.config['SQLALCHEMY_DATABASE_URI'])

catalogue_service = CatalogueService()
app_service = AppService()

def githubprefix (github_organization, appid, version):
    if version == 'development':
        return "https://github.com/" + github_organization +  "/" + appid + "/"
    else: 
        return "https://github.com/" + github_organization +  "/" + appid + "/tree/" + version + "/"

def rawgithubprefix (github_organization, appid, version):
    if version == 'development':
        return "https://raw.githubusercontent.com/" + github_organization +  "/" + appid + "/master/"
    else: 
        return "https://raw.githubusercontent.com/" + github_organization +  "/" + appid + "/" + version + "/"

def loadAndCheckJsonFromGit (url):
    #print (url)
    try:
        download = requests.get(url).content
        #print (download)
    except Exception:
        raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
    try:
        json_as_dict = simplejson.loads(download)
    except Exception:
       raise Exception('Report a miss configured JSON')
    json_again = simplejson.dumps(json_as_dict)  
    return json_again


def readallparams ():
    catalogueNames = ['bibbox', 'eB3Kit']  
    catalogueName = 'bibbox'  
    appVersions= {}
    for cn in catalogueNames:
      c = catalogue_service.catalogue (catalogueName)
      if c:
          apps = simplejson.loads(c.content)  
          appDescr = {}
          for app_groups in apps:
            for group_member in app_groups ['group_members']:
                app_name =  group_member ['app_name']
                appDescr[app_name]  = 'https://github.com/bibbox/' + app_name 
                for version in group_member ['versions']:
                    if app_name in  appVersions:
                        if version['docker_version'] not in appVersions[app_name]:
                            appVersions [app_name].append (version['docker_version'])
                    else:
                        appVersions [app_name] = [version['docker_version']]
                        
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

        print (appid, v)    
        v_rec = app_service.version (appid, v)

        if v_rec:
            v_rec.appinfo = appinfo
            v_rec.environment_parameters = envparam
            db.session.commit()     
        else:
            v_rec= BibboxApp (appid, v, appinfo, envparam)
            db.session.add(v_rec)
            db.session.commit()

if __name__ == "__main__":
    print("hello")
    readallparams()
