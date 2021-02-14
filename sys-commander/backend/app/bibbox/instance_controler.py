import os
import time
import random
import logging
import requests
import simplejson

from flask import current_app, render_template
from backend.app import app_celerey
from backend.app import db


from celery.task.control import inspect
from celery_singleton import Singleton

# thats the path inside the container !
DEFAULTPATH = "/opt/bibbox/instances/"


@app_celerey.task(bind=True,  name='instance.stopInstance')
def stopInstance (self, instanceDescr):
    pass

@app_celerey.task(bind=True, name='instance.startInstance')
def startInstance (self, instanceDescr):
    pass

@app_celerey.task(bind=True,  name='instance.copyInstance')
def copyInstance (self, instanceDescr):
    pass

@app_celerey.task(bind=True,  name='instance.installInstance')
def installInstance (self, instanceDescr):
    path = DEFAULTPATH + instanceDescr['instancename']
    try:
        os.mkdir(path)
        path = DEFAULTPATH + instanceDescr['instancename'] + "/instance.json"
        with open(path, 'w') as f: 
            simplejson.dump (instanceDescr, f)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
  

@app_celerey.task(bind=True,  name='instance.deleteInstance')
def deleteInstance (self, instanceDescr):
    path = DEFAULTPATH + instanceDescr['instancename']
    try:
        os.rmdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully deleted the directory %s " % path)

