#!/usr/bin/env python3

import os
import json
import yaml
import subprocess
from os.path import dirname, abspath
import traceback
import logging
import uuid
from datetime import datetime
import io
import requests

class AppController:


    """
    Section: Helperfunctions
    """


    def __init__(self):
        self.rootdir = dirname(dirname(abspath(__file__)))
        self.appPath = self.rootdir + '/application-instance'

    @staticmethod
    def createJobID():
        jobID = str(uuid.uuid1())
        dateObj = datetime.now()
        datestring = str(dateObj.year) + '-' + str(dateObj.month) + '-' + str(dateObj.day) + '-' + str(dateObj.microsecond)
        return jobID + datestring

    @staticmethod
    def createFolder(JobID, instanceName):
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        subprocess.Popen(['mkdir' , appPath + '/' + instanceName])
        subprocess.Popen(['touch' , appPath + '/' + instanceName + '/app.log'])

    @staticmethod
    def setUpLog(jobID, instanceName):
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        path = appPath + '/' + instanceName + '/'
        try:
            logging.basicConfig(filename= path + 'app.log', filemode='w+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
            
        except Exception:
            print(Exception)


    @staticmethod
    def checkExists(jobID, instanceName):
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if instanceName in os.listdir(appPath):
            exists = True
        else:
            exists = False
        return exists

    @staticmethod
    def checkLocked(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Ckeck if app is locked' )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if 'LOCK' in os.listdir(appPath + '/' + instanceName):
            locked = True
        else:
            locked = False
        return locked

    @staticmethod
    def setStatus(jobID, status, instanceName):
        logging.info(jobID + ' - ' + 'Set status to ' + status )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        subprocess.Popen(['touch' , appPath + '/' + instanceName + '/STATUS'])
        text_file = open(appPath + '/' + instanceName + '/STATUS', "w")
        text_file.write(status)
        text_file.close()

    @staticmethod
    def lock(jobID, instanceName):
        logging.debug(jobID + ' - ' + 'Locking app: ' + instanceName )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        subprocess.Popen(['touch' , appPath + '/' + instanceName + '/LOCK'])

    @staticmethod
    def downloadApp(exists,locked, jobID, instanceName,appName,version):
        logging.info(jobID + ' - ' + 'Downloading app: ' + appName + '/' + instanceName + ' V:' + version)
        try:
            if exists == True:
                raise Exception('The app you want to install does already exist!')
            os.system('git clone -b ' + version +  ' https://github.com/bibbox/' + appName + '.git application-instance/' + instanceName + '/repo/')
        except Exception:
            logging.exception( jobID + ' - An error occurred during downloading!')
    
    def setInfo(jobID, instanceName,appName,version):
        logging.info(jobID + ' - ' + 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        subprocess.Popen(['touch' , appPath + '/' + instanceName + '/INFO'])
        text_file = open(appPath + '/' + instanceName + '/INFO', "w")
        text_file.write(jobID + '\n' + appName + '\n' + instanceName + '\n' + version)
        text_file.close()


    def setProxyFiles(jobID, instanceName, containerName):
        logging.info(jobID + ' - ' + 'Set proxi files')
        rootdir = dirname(dirname(abspath(__file__)))
        proxyPath = rootdir + '/sys-proxy/'
        name = instanceName + '.conf'
        with open(proxyPath + 'template.conf') as template:
            file_content = template.read()
            file_content = file_content.replace("§§INSTANCEID", instanceName)
            file_content = file_content.replace("§§CONTAINERNAME", containerName)
            template = open( proxyPath + 'proxyconfig/' + name, 'w+')
            template.write(file_content)
            template.close()


    def readContainername(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Read Containername')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        composefile = open(appPath + '/' + instanceName +'/repo/docker-compose-template.yml', 'r').read()
        data = yaml.load(composefile)
        for k, v in data["services"].items():
            if 'container_name' in v:
                ContainerName = v.get('container_name')
                ContainerName = ContainerName.replace('§§INSTANCE', instanceName)
                try:
                    ContainerName = ContainerName.replace('-db', '')
                except:
                    pass

        return ContainerName



    """
    Section: Main functions
    """

    @staticmethod
    def getParamsold(instanceName):
        paramList = {}
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        with open(appPath + '.env') as f:
            file_content = f.read()
            words = file_content.split("\n")
            for line in words[:-2]:
                params = line.split('=')
                param = params[0]
                paramList[param] = []
        with open(rootdir + '/application-instance/' + instanceName +'/params.json', 'w+') as outfile:        
            json.dump(paramList, outfile)

    @staticmethod
    def readParams(instanceName):
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        with open(rootdir + '/application-instance/' + instanceName +'/params.json', 'w+') as json_file: 
            data = json.load(json_file)
            

    @staticmethod
    def getParams(instanceName, appName, version):
        url = 'https://raw.githubusercontent.com/bibbox/' + appName + '/master/.env'
        download = requests.get(url).content
        data=download.decode('utf-8')
        params = data.split('\n')
        paramList = {}
        for line in params:
            params = line.split('=')
            param = params[0]
            if param == 'PORT' or param == '' or param == 'INSTANCE':
                pass
            else:
                paramList[param] = []
            
        #paramList = json.dumps(paramList)
        
        return paramList, instanceName, appName, version

    @staticmethod
    def setParams(paramList):
        #data = json.load(paramList)
        for key in paramList:
            paramList[key] = 'ww'

        return paramList

    @staticmethod
    def writeCompose(jobID, paramList, instanceName):
        logging.info(jobID + ' - ' + 'Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        compose = open(appPath + '/docker-compose-template.yml', 'r').read()
        #compose = yaml.load(compose)
        for key in paramList:
            compose = compose.replace('§§' + key, paramList[key])
        compose = compose.replace('§§INSTANCE', instanceName)
        target = open(appPath + '/docker-compose-template.yml', 'w')
        target.write(compose)
        target.close()
        
    @staticmethod
    def composeUp(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Docker compose up')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        #subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose.yml', 'up', '-d '])
        os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml up -d ')

    @staticmethod
    def installApp(paramList, instanceName, appName, version):
        jobID = AppController.createJobID()
        exists = AppController.checkExists(jobID, instanceName)
        AppController.createFolder(jobID, instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.setStatus(jobID, 'Installing', instanceName)
        #exists = AppController.checkExists(jobID, instanceName)
        locked = AppController.checkLocked(jobID, instanceName)
        AppController.lock(jobID, instanceName)
        AppController.downloadApp(exists,locked, jobID, instanceName,appName,version)
        AppController.setInfo(jobID, instanceName,appName,version)
        containerName = AppController.readContainername(jobID, instanceName)
        AppController.setProxyFiles(jobID, instanceName, containerName)
        AppController.writeCompose(jobID, paramList, instanceName)
        AppController.composeUp(jobID, instanceName)

    



x = AppController()
paramList, instanceName, appName, version = x.getParams('testapp','app-seeddmsTNG','master')
paramList = x.setParams(paramList)

x.installApp(paramList, instanceName, appName, version)


