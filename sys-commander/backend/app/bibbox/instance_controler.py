import os
import time
import random
import logging
import requests
import simplejson
import yaml

from flask import current_app, render_template
from backend.app import app_celerey
from backend.app import db
#from backend.app.bibbox import compose_template


from celery.task.control import inspect
from celery_singleton import Singleton

# thats the path inside the container !
DEFAULTPATH = "/opt/bibbox/instances/"

def getBaseUrlRaw (version, app_name):
    burl = ''
    if version == 'development':
        burl = 'https://raw.githubusercontent.com/bibbox/' + app_name   + '/master/'
    else:
        burl = 'https://raw.githubusercontent.com/bibbox/' + app_name   + '/' + version + '/'
    return burl



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
    # appinfo.json, fileinfo.json, docker-compose-template.yml, 

    try:
        os.mkdir(path)
        path = DEFAULTPATH + instanceDescr['instancename'] + "/instance.json"
        with open(path, 'w') as f: 
            simplejson.dump (instanceDescr, f)
        instanceDescr['state'] = 'INSTALLING'
        with open(path, 'w') as f: 
            simplejson.dump (instanceDescr, f)

        app_name = instanceDescr['appname']
        version = instanceDescr['version']
        filename = getBaseUrlRaw (app_name, version) + 'docker-compose-template.yml'

        # testing
        # path_to_template = str(os.path.dirname(os.path.realpath(__file__))) + "/test_output/"
        # with open(path_to_template + "docker-compose-template-testing.yml", 'r') as template_obj:
        #     template_str = template_obj.read()
        #     compose_class_instance = ComposeTemplate(template_str, [instanceDescr['instancename'], "test_pw", DEFAULTPATH])

    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
  

@app_celerey.task(bind=True,  name='instance.deleteInstance')
def deleteInstance (self, instanceDescr):
    path = DEFAULTPATH + instanceDescr['instancename']
    try:

        # hier kommt alles andere davor 
        os.rmdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully deleted the directory %s " % path)


# import uuid
# import requests
# if __name__ == "__main__":
#     print ("====================== INSTANCE CONTROLOER DEVELOPMENT TEST =====================")

#     res = requests.get('http://127.0.0.1:5010/api/v1/instances')
#     print ('response from server:',res.text)

#     print("try to call")
#     paylod = {
#         "appname"     : "app-wordpress",
#         "version"     :  "V4",
#         "displayname" : "Wordpress Test",
#         "dataroot"    : '/opt/bibbox/instance-data/',
#         "parameters"  : 
#             {
#                 'MYSQL_ROOT_PASSWORD' :'quaksi'
#             }            
#     }
#     res = requests.post('http://127.0.0.1:5010/api/v1/instances/' + str(uuid.uuid4()), json=paylod)
#     print ('response from server:',res.text)
#     print ("======================              DONE                     ====================")

    
