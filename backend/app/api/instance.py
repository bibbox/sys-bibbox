import os
import json
import docker

from flask import Flask, request
from flask_restplus import Namespace, Api, Resource, fields
from backend.app import app, db, restapi

from backend.app.bibbox.instance_controler  import installInstance, startInstance, stopInstance, restartInstance, deleteInstance, testProcessAsync, updateInstanceInfos
from backend.app.bibbox.file_handler import FileHandler
from backend.app.bibbox.docker_handler import DockerHandler


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
# this should only be used in the file_handler
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


@api.route('/stop/<string:id>')
@api.doc("Stop all Instance Containers")
class Ping(Resource):
    def get(self, id):
        
        stopInstance.delay(id)

        return {"stopping instance": id}, 200

@api.route('/start/<string:id>')
@api.doc("Start all Instance Containers")
class Ping(Resource):
    def get(self, id):
        
        startInstance.delay(id)

        return {"starting instance": id}, 200

@api.route('/restart/<string:id>')
@api.doc("Restart all Instance Containers")
class Ping(Resource):
    def get(self, id):
        
        restartInstance.delay(id)

        return {"restarting instance": id}, 200



@api.route('/')
class InstanceList(Resource):
    def get(self):
        # should we put in an own class ?, maybe yes ...
        fh = FileHandler()
        # TODO - error if file does not exist

        try: 
            fh.writeInstancesJsonFile()
            result = json.loads(fh.getInstancesJSONFile())
        except:
            result = []

        return result, 200


@api.route('/<string:id>')
@api.doc(params={'id': 'An ID'})
class Instance(Resource):
    
    def get(self, id):
        fh = FileHandler()
        idescr = fh.getInstanceJSONContent(id)
        return idescr, 200


    @api.doc(responses={403: 'Not Authorized'})
    @api.doc(responses={ 202: 'Accepted', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={ 'id': 'Instance ID' })
    def post(self, id):

        instanceDescr = request.json
        instanceDescr['instancename'] = id
        instanceDescr['state'] = 'JUSTBORN'
        instanceDescr['displayname_long'] = ''    
        instanceDescr['description_short'] = ''   
        instanceDescr['description_long'] = ''  
        
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

        fh = FileHandler()
        instanceToBeDeleted = fh.getInstanceJSONContent(instancename)
    
        message =  {
              "task": {
                "href": jobURL,
                "id": jobID
                },
             "instance" :  instanceToBeDeleted,
        }

        deleteInstance.delay(instancename)



        return message, 202    


    @api.doc("Patch instance.json values. Requires a dict of key-value pairs to update.")
    def patch(self, id):
        
        instance_name = id
        payload = request.json

        jobID = 27
        jobURL = "api/v1/activities/27"

        fh = FileHandler()
        instanceToBeUpdated = fh.getInstanceJSONContent(instance_name)
        message = {
            "task": {
                "href": jobURL,
                "id": jobID
                },
            "instance" :  instanceToBeUpdated,
        }

        updateInstanceInfos.delay(instance_name, payload)

        return message, 202


@api.route('/logs/<string:id>')
@api.doc(params={'id': 'An ID'})
class Instance(Resource):
    def get(self, id):
        logs = {}

        try:
            dh = DockerHandler()
            logs = dh.docker_getContainerLogs(id)

        except Exception as ex:
            print(ex)
            logs = {'error': ex}


        return logs, 200

@api.route('/names/<string:name_to_check>')
@api.doc(params={'name_to_check': 'Instancename to check'})
class Instance(Resource):
    def get(self, name_to_check):
        name_to_check = str(name_to_check).lower()
        fh = FileHandler()
        res = 'false'
        try:
            names = fh.getInstanceNames()
            if name_to_check in names:
                res = 'true'
        except Exception as ex:
            print(ex)
            res = [str(ex)]


        return res, 200
