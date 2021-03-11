import os
import json

from flask import Flask, request
from flask_restplus import Namespace, Api, Resource, fields
from backend.app import app, db, restapi

from backend.app.bibbox.instance_controler  import installInstance, stopInstance, deleteInstance, testProcessAsync
from backend.app.bibbox.file_manager import FileManager

api = Namespace('instances', description='Instance Ressources')
restapi.add_namespace (api, '/instances')

instancemodel = api.model('Model', {
    'instancename' : fields.String,
    'appname': fields.String,
    'version' :  fields.String,
    'state' : fields.String
})

# TODO
# thats the path inside the container !
# this should only be used in the file_manager
INSTANCEPATH = "/opt/bibbox/instances/"

def instanceDesc ():
    path = INSTANCEPATH + instanceDescr['instancename'] + "/instance.json"
    with open(path) as f: 
        idescr = json.load(f)
    return idescr

@api.route('/ping')
@api.doc(params={'murks': 'test'})
@api.doc("Just to test if the Instance API is alive")
class Ping(Resource):
    def get(self):
        return {"reply":"PONG"}

@api.route('/pong')
@api.doc("Test a async Process through the Instance API")
class Ping(Resource):
    def get(self):
        testProcessAsync.delay()
        return {"reply":"PING"}

@api.route('/')
class InstanceList(Resource):
    def get(self):
        # should we put in an own class ?, maybe yes ...
        fm = FileManager()
        # TODO - error if file does not exist

        try: 
            result = json.loads(fm.getInstancesJSONFile())
        except:
            result = []

        return result, 200


@api.route('/<id>')
@api.doc(params={'id': 'An ID'})
class Instance(Resource):
    
    def get(self):
        idescr = json.load(id)
        return idescr, 200


    @api.doc(responses={403: 'Not Authorized'})
    @api.doc(responses={ 202: 'Accepted', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={ 'id': 'Instance ID' })
    def post(self, id):

        instanceDescr = request.json
        instanceDescr['instancename'] = id
        instanceDescr['state'] = 'JUSTBORN'    

        jobID = 27
        jobURL = "api/v1/activities/27"

        installInstance.delay ( instanceDescr )

        message =  {
              "task": {
                "href": jobURL,
                "id": jobID
                },
             "instance" :  instanceDescr        
        }
        return message, 202

    def delete(self, id):

        # make this more dynamic and check the parameters
        instancename = id

        jobID = 27
        jobURL = "api/v1/activities/27"

        # call the deletion of a instance
        appname = "get instance JSON from the instance controler, which simply reads the instance.json file in the instance directory"

        fm = FileManager()
        instanceToBeDeleted = fm.getInstanceJSONContent(instancename)

        # this should execute first
        stopInstance.delay(instancename)

        # remove if race condition is fixed
        import time
        time.sleep(8)

        # this should execute only after stopInstance has finished executing
        deleteInstance.delay(instancename)


        message =  {
              "task": {
                "href": jobURL,
                "id": jobID
                },
             "instance" :  instanceToBeDeleted,
             "status": "PLACEHOLDER"        
        }

        return message, 202    
