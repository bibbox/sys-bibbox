import os
import re
import time
import copy
import yaml
import random
import logging
import requests
import simplejson
import subprocess


from flask import current_app, render_template
from backend.app import app_celerey
from backend.app import db

from backend.app.services.activity_service import ActivityService
from backend.app.services.db_logger_service import DBLoggerService

from backend.app.bibbox.instance_handler import InstanceHandler
from backend.app.bibbox.file_handler import FileHandler
from backend.app.bibbox.instance import Instance
from backend.app.bibbox.docker_handler import DockerHandler

from celery.task.control import inspect
from celery_singleton import Singleton

# thats the path inside the container !
INSTANCEPATH = "/opt/bibbox/instances/"
PROXYPATH    = "/opt/bibbox/proxy/sites/"


@app_celerey.task(bind=True,  name='instance.stopInstance')
def stopInstance (self, instanceName):
    dh = DockerHandler();
    dh.docker_stopInstance(instanceName)

@app_celerey.task(bind=True, name='instance.startInstance')
def startInstance (self, instanceName):
    pass

@app_celerey.task(bind=True,  name='instance.copyInstance')
def copyInstance (self, instanceNameSrc, instanceNameDest):
    pass

@app_celerey.task(bind=True,  name='instance.installInstance')
def installInstance (self, instanceDescr):
    path = INSTANCEPATH + instanceDescr['instancename']
    # appinfo.json, fileinfo.json, docker-compose-template.yml, 
    
    file_handler = FileHandler()

    # check if directory structure is valid, fixes structure if invalid
    # needs to be called sooner, but where/when?
    file_handler.checkDirectoryStructure()


    # activity service for db-stuff with activity entries
    activity_service = ActivityService()
    
    # create activity entry in db -> returns ID of created entry 
    activity_id = activity_service.create(f"Install instance: {instanceDescr['instancename']}", "INSTALL_INSTANCE")

    # logger service for creating custom logger
    logger_serv = DBLoggerService(activity_id, f"[INSTALL] {instanceDescr['instancename']}")
    logger = logger_serv.getLogger()


    # generate the instance directory    
    try:
        try:
            os.mkdir(path)
            path = INSTANCEPATH + instanceDescr['instancename'] + "/instance.json"
            with open(path, 'w') as f:       
                instanceDescr['state'] = 'INSTALLING'
                instanceDescrInTheFile =  copy.deepcopy(instanceDescr)
                del instanceDescrInTheFile['parameters']
                simplejson.dump (instanceDescrInTheFile, f)
        except OSError:
            #print ("Creation of the directory %s failed" % path)
            logger.error("Creation of the directory {} failed".format(instanceDescr['instancename'] + "/instance.json"))
        else:
            #print ("Successfully created the directory %s " % path)
            logger.info("Successfully created the directory {}.".format(instanceDescr['instancename'] + "/instance.json"))
    
        # copy all file from the APP repository to the instance Directory
        file_handler.copyAllFilesToInstanceDirectory (instanceDescr)

        # now we can generate an Instance object
        instance = Instance (instanceDescr['instancename'])


        compose_file_name = INSTANCEPATH + instanceDescr['instancename'] + "/docker-compose.yml"
        proxy_file_name   = PROXYPATH    + '005-' + instanceDescr['instancename'] + ".conf"

        # generate the docker-compose file
        try:
            template_str = instance.composeTemplate()    
            instance_handler =  InstanceHandler (template_str, instanceDescr)
            docker_compose = yaml.dump(instance_handler.getCompose(), default_flow_style=False) 
            with open(compose_file_name, 'w') as f:       
                f.write ( docker_compose )
        except:
            #print ("ERROR in the generation of the Docker Compose" )
            logger.error("Creation of the {} docker-compose file failed.".format(instanceDescr['instancename'] + "/docker-compose.yml"))
            raise
        else:
            #print ("Successfully created the docker-compose" )
            logger.info("Successfully created the {} docker-compose file.".format(instanceDescr['instancename'] + "/docker-compose.yml"))

        # write the proxy file
        try:
            template_str = instance.composeTemplate()    
            instance_handler =  InstanceHandler (template_str, instanceDescr)
            instance_handler.generateProxyFile()
        except:
            #print ("ERROR in the generation of the Proxy File" )
            logger.error("Creation of the {} proxy file failed".format('005-' + instanceDescr['instancename'] + ".conf"))
            raise
        else:
            #print ("Successfully created the proxy file" )
            logger.info("Successfully created the {} proxy file.".format('005-' + instanceDescr['instancename'] + ".conf"))

        # write the instances.json file
        try:
            file_handler.writeInstancesJsonFile()
        except:
            #print (" ERROR in the generation of the instances.json File")
            logger.error("Creation of the instances.json file failed")
            raise
        else:
            #print ("Successfully created the instances.json File")
            logger.info("Successfully created the instances.json file")


        # testing to update instance json 
        file_handler.updateInstanceJsonState(instanceDescr['instancename'], "INSTALLING")
        file_handler.updateInstanceJsonProxy(instanceDescr['instancename'], instance_handler.getProxyInformation())


        # call docker-compose up
        print (compose_file_name)
        # process = subprocess.Popen(['ls', '-la', '/opt/bibbox/instances'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
        process = subprocess.Popen(['docker-compose', '-f', compose_file_name, 'up', '-d'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")

        # TOOO
        # put this in a helper function for calling system commands
        ansi_regex = r'\x1b+\[+\d+\d+;+\d+\d+[m]|' \
                r'\x1b(' \
                r'(\[\??\d+[hl])|' \
                r'([=<>a-kzmNM78])|' \
                r'([\(\)][a-b0-2])|' \
                r'(\[\d{0,2}[ma-dgkjqi])|' \
                r'(\[\d+;\d+[hfy]?)|' \
                r'(\[;?[hf])|' \
                r'(#[3-68])|' \
                r'([01356]n)|' \
                r'(O[mlnp-z]?)|' \
                r'(/Z)|' \
                r'(\d+)|' \
                r'(\[\?\d;\d0c)|' \
                r'(\d;\dR)|' \
                r'(\[*\d*\d*;*\d*\d*[m]))' 
                
        ansi_escape = re.compile(ansi_regex, flags=re.IGNORECASE)

        while True:
            line = process.stdout.readline()
            lineerror = process.stderr.readline()
            if not line and not lineerror:
                break
            #the real code does filtering here
            if line:
                # look what we have to strip 
                # if there are some escape code, that the öine is overwritten, the last line in the log should be replaced
                result = ansi_escape.sub('', line).rstrip()
                print (line.rstrip())
                print (result)
            if lineerror:
                # same stuff here, also write this in the log file
                print (lineerror.rstrip())

        # restart apache
        # TODO make a reload instead a restart
        logger.info("restarting bibbox-sys-commander-apacheproxy...")
        process = subprocess.Popen(['docker', 'restart', 'bibbox-sys-commander-apacheproxy'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
        while True:
            line = process.stdout.readline()
            lineerror = process.stderr.readline()
            if not line and not lineerror:
                break
            #the real code does filtering here
            if line:
                # look what we have to strip 
                # if there are some escape code, that the öine is overwritten, the last line in the log should be replaced
                result = ansi_escape.sub('', line).rstrip()
                print (line.rstrip())
                print (result)
            if lineerror:
                # same stuff here, also write this in the log file
                print (lineerror.rstrip())

    except Exception as ex:
        print(ex)
        activity_service.update(activity_id, "ERROR", "FAILURE")
    else:
        activity_service.update(activity_id, "FINISHED", "SUCCESS")


@app_celerey.task(bind=True,  name='instance.deleteInstance')
def deleteInstance (self, instance_name):

    dh = DockerHandler()        
    fh = FileHandler()
    instance_path = fh.INSTANCEPATH + instance_name

    # activity service for db-stuff with activity entries
    activity_service = ActivityService()
    
    # create activity entry in db -> returns ID of created entry 
    activity_id = activity_service.create(f"Delete instance: {instance_name}", "DELETE_INSTANCE")

    # logger service for creating custom logger
    logger_serv = DBLoggerService(activity_id, f"[DELETE] {instance_name}")

    # get custom logger from logger service
    logger = logger_serv.getLogger()

    try:
        try:
            stopInstance(instance_name)
        except OSError:
            print ("Stopping {} containers failed.".format(instance_name))
            logger.error("Stopping {} containers failed".format(instance_name))
        else:
            print ("Successfully stopped the {} containers".format(instance_name))
            logger.info("Successfully stopped the {} containers".format(instance_name))

        try:
            dh.docker_deleteStoppedContainers(instance_name)
        except OSError:
            print ("Deletion of stopped {} containers failed".format(instance_name))
            logger.error("Deletion of stopped {} containers failed".format(instance_name))
        else:
            print ("Successfully deleted the {} containers".format(instance_name))
            logger.info("Successfully deleted the {} containers".format(instance_name))
        
        try:       
            fh.removeAllFilesInDir(instance_path)
        except OSError:
            print ("Deletion of the directory {} failed".format(instance_name))
            logger.error("Deletion of the directory {} failed".format(instance_name))
        else:
            print ("Successfully deleted the directory {} ".format(instance_name))
            logger.info("Successfully deleted the directory {} ".format(instance_name))


        try:
            fh.removeProxyConfigFile(instance_name)
        except OSError:
            print ("Deletion of the proxy file of {} failed".format(instance_name))
            logger.error("Deletion of the proxy file of {} failed".format(instance_name))
        else:
            print ("Successfully deleted the proxy file of {} ".format(instance_name))
            logger.info("Successfully deleted the proxy file of {} ".format(instance_name))
    
        activity_service.update(activity_id, "FINISHED", "SUCCESS")

    except Exception as ex:
        activity_service.update(activity_id, "ERROR", "FAILURE")
    
    
    

# TODO
# make this a helper function, with the stripping 
def testProcess():
    print ('XXXXXXXXXXXXXXXXXXXXXXXXX')
    process = subprocess.Popen(['docker-compose', '-f', '/opt/bibbox/instances/wptest02/docker-compose.yml', 'up', '-d'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
    i = 0
    while True:
        line = process.stdout.readline()
        lineerror = process.stderr.readline()

        if not line and not lineerror:
            break
        #the real code does filtering here
        if line:
            print (line.rstrip())
        if lineerror:
            print ("error", lineerror.rstrip())
        i = i+1
    print ('DONE')

@app_celerey.task(bind=True,  name='instance.testProcessAsny')
def testProcessAsync (self):
    testProcess()


if __name__ == "__main__":  
#    print ('TEST the subprocess.Popen ')
#    testProcess()
    print ('TEST the subprocess.Popen with CELERY')
    testProcessAsync.delay()
    print ('TEST DONE')

'''

    i = Instance ('06-wptest')

    template_str = i.composeTemplate()  

    payload = {
        "instancename" : "06-wptest",
        "displayname" : "Wordpress Test",
        "app" : {
            "organization": "bibbox",
            "name"        : "app-wordpress",
            "version"     : "V4",
        },
        "parameters"  : 
            {
                "MYSQL_ROOT_PASSWORD" : "quaksi"
            }            
    }
    
    instance_handler =  InstanceHandler (template_str, payload)
    dc = bb_configurator.getCompose()
    dc = yaml.dump(bb_configurator.getCompose(), default_flow_style=False)
    #print (dc)

    compose_file_name = INSTANCEPATH + payload['instancename'] + "/docker-compose.yml"

    print ( compose_file_name )
    process = subprocess.Popen(['docker-compose', '-f', compose_file_name, 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    
    with process.stdout:
        for line in iter(process.stdout.readline, b''): 
            print (line) 

    print ( "DONE" )
'''    
