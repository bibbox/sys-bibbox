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
    def checkExists(jobID, instanceName, install):
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if instanceName in os.listdir(appPath):
            exists = True
        else:
            exists = False
        if install == True:
            if exists == True:
                raise Exception('The app you want to install does already exist!')
        if install == False:
            if exists == False:
                raise Exception('The app you want to use does not exist!')

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
            logging.basicConfig(filename= path + 'app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
            
        except Exception:
            print(Exception)


    @staticmethod
    def setStatus(jobID, status, instanceName):
        logging.info(jobID + ' - ' + 'Set status to ' + status )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        process = subprocess.Popen(['touch' , appPath + '/' + instanceName + '/STATUS'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output) )
        text_file = open(appPath + '/' + instanceName + '/STATUS', "w")
        text_file.write(status)
        text_file.close()

    @staticmethod
    def lock(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Ckeck if app is locked' )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if 'LOCK' in os.listdir(appPath + '/' + instanceName):
            with open(appPath + '/' + instanceName + '/LOCK') as lockfile:
                lockID = lockfile.read()
                if lockID != jobID:
                    logging.exception( jobID + ' - The app you want to use is currently locked! Please try again later!')
                    raise Exception('The app you want to use is currently locked! Please try again later!')

        logging.debug(jobID + ' - ' + 'Locking app: ' + instanceName )
        process = subprocess.Popen(['touch' , appPath + '/' + instanceName + '/LOCK'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output) )
    
    @staticmethod
    def unlock(jobID, instanceName):
        logging.debug(jobID + ' - ' + 'Unlocking app: ' + instanceName )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        process = subprocess.Popen(['rm' , appPath + '/' + instanceName + '/LOCK'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output) )

    @staticmethod
    def downloadApp(jobID, instanceName,appName,version):
        logging.info(jobID + ' - ' + 'Downloading app: ' + appName + '/' + instanceName + ' V:' + version)
        
        process = subprocess.Popen(['git', 'clone','-b', version, 'https://github.com/bibbox/' + appName + '.git', 'application-instance/' + instanceName + '/repo/'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.exception(jobID + str(output) )
    
    @staticmethod
    def setInfo(jobID, instanceName,appName,version):
        logging.info(jobID + ' - ' + 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        process = subprocess.Popen(['touch' , appPath + '/' + instanceName + '/INFO'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        text_file = open(appPath + '/' + instanceName + '/INFO', "w")
        text_file.write(jobID + '\n' + appName + '\n' + instanceName + '\n' + version)
        text_file.close()

    @staticmethod
    def setProxyFiles(jobID, instanceName, containerName):
        logging.info(jobID + ' - ' + 'Set proxy files')
        rootdir = dirname(dirname(abspath(__file__)))
        proxyPath = rootdir + '/sys-proxy/'
        name = instanceName + '.conf'
        with open(proxyPath + 'template.conf') as template:
            file_content = template.read()
            file_content = file_content.replace("§§INSTANCEID", instanceName)
            file_content = file_content.replace("§§CONTAINERNAME", containerName)
            template = open( proxyPath + 'proxyconfig/sites/' + name, 'w+')
            template.write(file_content)
            template.close()

    @staticmethod
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
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['docker', 'exec', '-it', 'local_nginx', 'service', 'nginx', 'reload'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))

    @staticmethod
    def stop(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Stopping App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'stop'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        #os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml stop ')

    @staticmethod
    def start(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Starting App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'start'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        #os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml start ')

    @staticmethod
    def remove(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Romoving App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        #os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml down ')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'down'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['sudo', 'chmod' ,'-f', '-R', '777', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['rm' , '-f', '-R', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['rm' , '-f', rootdir + '/sys-proxy/proxyconfig/sites/' + instanceName + '.conf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))

    @staticmethod
    def status(jobID, instanceName):
        logging.info(jobID + ' - ' + 'Reading Status of App: ' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/'
        with open(appPath + 'STATUS') as statusfile:
            file_content = statusfile.read()
        return file_content

    @staticmethod
    def checkStatus(jobID, instanceName, statusList):
        logging.info(jobID + ' - ' + 'Checking if operation is possible for current state of app: ' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/'
        with open(appPath + 'STATUS') as statusfile:
            file_content = statusfile.read()
        if file_content not in statusList:
            logging.exception(jobID + ' - ' + 'Current app status does not allow operation on app: ' + instanceName)
            raise Exception('Current app status does not allow your operation!')

    @staticmethod
    def copy(jobID, instanceName, newName):
        logging.info(jobID + ' - ' + 'Copy App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        process = subprocess.Popen(['sudo', 'cp', '-r', rootdir + '/application-instance/' + instanceName, rootdir + '/application-instance/' + newName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))

    @staticmethod
    def changeCompose(jobID, paramList, instanceName, newName):
        logging.info(jobID + ' - ' + 'Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        compose = open(appPath + '/docker-compose-template.yml', 'r')#.read()
        compose = yaml.load(compose)
        services = compose['services']
        for service in services:
            name = services[service]['container_name']
            newContainerName = name.replace(instanceName, newName)
            services[service]['container_name'] = newContainerName
        yaml.dump()

        pass


        
    """
    Section: Main functions
    """

    @staticmethod
    def getParams(instanceName, appName, version):
        try:
            url = 'https://raw.githubusercontent.com/bibbox/' + appName + '/master/.env'
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
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
            
        return paramList, instanceName, appName, version

    @staticmethod
    def setParams(paramList):
        #data = json.load(paramList)
        for key in paramList:
            paramList[key] = 'ww'

        return paramList

    
    @staticmethod
    def installApp(paramList, instanceName, appName, version):
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install = True)
        AppController.createFolder(jobID, instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.setStatus(jobID, 'Prepare Install', instanceName)
        #exists = AppController.checkExists(jobID, instanceName)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Downloading', instanceName)
        AppController.downloadApp(jobID, instanceName,appName,version)
        AppController.setStatus(jobID, 'Installing', instanceName)
        AppController.setInfo(jobID, instanceName,appName,version)
        containerName = AppController.readContainername(jobID, instanceName)
        AppController.setProxyFiles(jobID, instanceName, containerName)
        AppController.writeCompose(jobID, paramList, instanceName)
        AppController.composeUp(jobID, instanceName)
        AppController.unlock(jobID, instanceName)
        AppController.setStatus(jobID, 'Running', instanceName)
    
    @staticmethod
    def stopApp(instanceName):
        statusList = ['Running']
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        AppController.checkStatus(jobID, instanceName, statusList)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Stopping', instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.stop(jobID, instanceName)
        AppController.unlock(jobID, instanceName)
        AppController.setStatus(jobID, 'Stopped', instanceName)

    @staticmethod
    def startApp(instanceName):
        statusList = ['Stopped']
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        AppController.checkStatus(jobID, instanceName, statusList)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Starting', instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.start(jobID, instanceName)
        AppController.unlock(jobID, instanceName)
        AppController.setStatus(jobID, 'Running', instanceName)

    @staticmethod
    def removeApp(instanceName):
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Removing App', instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.remove(jobID, instanceName)

    @staticmethod
    def getStatus(instanceName):
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        AppController.setUpLog(jobID, instanceName)
        AppController.status(jobID, instanceName)

    @staticmethod
    def copyApp(instanceName, newName):
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        AppController.lock(jobID, instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.copy(jobID, instanceName, newName)
        AppController.setUpLog(jobID, newName)
        AppController.changeCompose(jobID, paramList, instanceName, newName)
        AppController.unlock(jobID, instanceName)

x = AppController()
paramList, instanceName, appName, version = x.getParams('testapp','app-seeddmsTNG','master')
paramList = x.setParams(paramList)

#x.installApp(paramList, instanceName, appName, version)
#status = x.getStatus(instanceName)
#x.stopApp(instanceName)
#x.startApp(instanceName)
#x.removeApp(instanceName)
x.copyApp('testapp', 'testappnew')
