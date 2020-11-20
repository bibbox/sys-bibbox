#!/usr/bin/env python3

import os
import json
import sys
import yaml
import subprocess
from os.path import dirname, abspath
import traceback
import logging
import logging.handlers
import uuid
from datetime import datetime
import io
import requests
import copy
from os import path
from subprocess import check_output
import simplejson
import re
import atexit
from packaging import version
import time



__author__ = "Stefan Herdy"
__credits__ = ["Heimo Müller", "Robert Reihs ", "Markus Plass",]
__license__ = "..."
__version__ = "1.0.1"
__email__ = "stefan.herdy@medunigraz.at"
__status__ = "Development"



class AppController:

    def __init__(self):
        self.rootdir = dirname(dirname(abspath(__file__)))
        self.appPath = self.rootdir + '/application-instance'
        with open(self.rootdir + '/environment-parameters.json') as infofile:
            params = json.load(infofile)
            domain = params[0]['DOMAIN_NAME']
        
    def __del__(self):
        try:
            jobID = AppController.createJobID(self)
            instanceName = self.instanceName
            AppController.unlock(self, jobID, instanceName, end = True)
        except:
            pass

    def createJobID(self):
        '''
        Description:
        -----------
        Creates a unique JobID to be able to identify every single job.

        Parameters:
        ----------

        Raises:
        -------
        
        Returns:
        -------
        Job ID : str
            Unique JobID that consists of an uuid and the current datetime
        '''
        jobID = str(uuid.uuid1())
        dateObj = datetime.now()
        datestring = str(dateObj.year) + '-' + str(dateObj.month) + '-' + str(dateObj.day) + '-' + str(dateObj.microsecond)
        jobID = jobID + datestring
        return jobID

    def checkExists(self, jobID, instanceName, install):
        '''
        Description:
        -----------
        Checks if an app with the wanted name does already exist.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        install: bool
            Is the method performed during Installation?
            For installation, its necessary that the app does not exist, 
            but for start, stop, coppy ... of an app it is important that the app already exists.

        Raises:
        -------
        if install == True:

            if exists == True

                raise Exception('The app you want to install does already exist!')

        if install == False:

            if exists == False:

                raise Exception('The app you want to use does not exist!')

        Returns:
        -------
        
        '''
        rootdir = dirname(dirname(abspath(__file__)))
        bibbox_logger = AppController.setUpLog(self, jobID, instanceName, systemonly=True)
        appPath = rootdir + '/application-instance/'
        bibbox_logger.info('Check if app folder exists')
        if path.exists(appPath) == False:
            process = subprocess.Popen(['mkdir', appPath])
            output, error = process.communicate()
            if output:
                bibbox_logger.debug( str(output))
        if instanceName in os.listdir(appPath):
            exists = True
        else:
            exists = False
        if install == True:
            if exists == True:
                bibbox_logger.info('The app you want to install does already exist! App: ' + instanceName)
                raise Exception('The app you want to install does already exist! App: ' + instanceName)
        if install == False:
            if exists == False:
                bibbox_logger.info('The app you want to use does not exist! App: ' + instanceName)
                raise Exception('The app you want to use does not exist! App: ' + instanceName)

    def createFolder(self, jobID, instanceName):
        '''
        Description:
        -----------
        Creates destination folder for app repository.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------
        

        Returns:
        -------
        
        '''
        bibbox_logger = AppController.setUpLog(self, jobID, instanceName, systemonly=True)
        bibbox_logger.info('Check if app folder exists')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            bibbox_logger.error( 'Error While creating folder for application ' + instanceName + '. The folder "/application-instance" does not exist!')
            raise Exception('Error While creating folder for application ' + instanceName + '. The folder "/application-instance" does not exist!')
        process = subprocess.Popen(['mkdir' , appPath + '/' + instanceName])
        output, error = process.communicate()
        if output:
            bibbox_logger.debug( str(output))
        process = subprocess.Popen(['mkdir' , appPath + '/' + instanceName + '/log/'])
        output, error = process.communicate()
        if output:
            bibbox_logger.debug( str(output))
        if path.exists(appPath + '/' + instanceName) == False:
            bibbox_logger.error( 'Error While creating folder for application ' + instanceName + '. The folder "/application-instance/' + instanceName + '/" does not exist!')
            raise Exception('Error While creating folder for application ' + instanceName + '. The folder "/application-instance" does not exist!')
        if path.exists(appPath + '/' + instanceName + '/log/') == False:
            bibbox_logger.error( 'Error While creating folder for application ' + instanceName + '. The folder "/application-instance' + instanceName + '/log/" does not exist!')
            raise Exception('Error While creating folder for application ' + instanceName + '. The folder "/application-instance" does not exist!')

    def setup_logger(self, jobID, loggerName, log_file, level=logging.DEBUG):
        '''
        Description:
        -----------
        Sets up logger.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        loggerName : str
            Name of the logger 

        logfile : str
            Path like object that defines the logfile destination and the logfile's name
        
        Raises:
        -------
        

        Returns:
        -------
        
        '''
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        logformatter = logging.Formatter(jobID + '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        logger = logging.getLogger(loggerName)
        if logger.handlers[:] == []:
            handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=20000000, backupCount = 10)
            handler.setFormatter(logformatter)
            stream = logging.StreamHandler()
            stream.setFormatter(formatter)
            logger.addHandler(stream)
            logger.addHandler(handler)
        logger.setLevel(level)

        return logger
    
    def setUpLog(self, jobID, instanceName, systemonly = False):
        '''
        Description:
        -----------
        Sets up initial log settings, such as format, file name etc.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------
        

        Returns:
        -------
        
        '''
        rootdir = dirname(dirname(abspath(__file__)))
        if systemonly == False:
            appPath = rootdir + '/application-instance'
            if path.exists(appPath) == False:
                raise Exception( ' - The folder "/application-instance/" does not exist!')
            logpath = appPath + '/' + instanceName + '/log/'
            if path.exists(logpath) == False:
                raise Exception( ' - The folder "/application-instance/' + instanceName + '/log/" does not exist!')
            os.system('sudo chmod 777 ' + logpath + '*')
            app_logger = AppController.setup_logger(self, jobID, instanceName + '-app.log', logpath + 'debug.log', level=logging.DEBUG)
            app_errorlogger = AppController.setup_logger(self, jobID, instanceName + '-apperror.log', logpath + 'error.log', level=logging.DEBUG)
            docker_logger = AppController.setup_logger(self, jobID, instanceName + '-docker.log', logpath + 'docker.log', level=logging.DEBUG)
            bibbox_logger = AppController.setup_logger(self, jobID, instanceName + '-bibbox.log', rootdir + '/log/system.log', level=logging.DEBUG)
            
            if path.exists(logpath + 'debug.log') == False:
                raise Exception('Error while creating logfile "debug.log" in folder ' + logpath + '.')
            if path.exists(logpath + 'error.log') == False:
                raise Exception('Error while creating logfile "error.log" in folder ' + logpath + '.')
            if path.exists(logpath + 'docker.log') == False:
                raise Exception('Error while creating logfile "docker.log" in folder ' + logpath + '.')
            if path.exists(rootdir + '/log/system.log') == False:
                raise Exception('Error while creating logfile "system.log" in folder ' + logpath + '.')
            
            return app_logger, bibbox_logger, docker_logger, app_errorlogger
        else:
            bibbox_logger = AppController.setup_logger(self, jobID, instanceName + 'bibbox', rootdir + '/log/system.log', level=logging.DEBUG)
            if path.exists(rootdir + '/log/system.log') == False:
                raise Exception('Error while creating logfile "system.log"')
            
            return bibbox_logger

    
    def setStatus(self, jobID, status, instanceName):
        '''
        Description:
        -----------
        Sets the current ststus of an app and writes it to a file calles STATUS.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        status: str
            The wanted ststus that gets written to the STATUS file

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------
        

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info('Set status to ' + status )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error( ' - The folder "/application-instance" does not exist!')
        process = subprocess.Popen(['touch' , appPath + '/' + instanceName + '/STATUS'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            app_errorlogger.error( str(output))
        try:
            text_file = open(appPath + '/' + instanceName + '/STATUS', "w")
            text_file.write(status)
            text_file.close()
        except Exception:
            app_errorlogger.exception('Fatal error in writing to STATUS file: ', exc_info=True)
            raise Exception('Fatal error in writing to STATUS file: ')
        if path.exists(appPath + '/' + instanceName + '/STATUS') == False:
            app_errorlogger.exception('Something went wrong during writing to STATUS file: ', exc_info=True)
            raise Exception('Fatal error in writing to STATUS file: ')


    def lock(self, jobID, instanceName):
        '''
        Description:
        -----------
        Creates a file named LOCK to lock an app, so that no one is able to perform other operations
        on an app before the current operation is finished.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------
        Exception('The app you want to use is currently locked! Please try again later!') if the wanted app is currently locked.

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Ckeck if app is locked' )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error(' - The folder "/application-instance" does not exist!')
        if 'LOCK' in os.listdir(appPath + '/' + instanceName):
            try:
                with open(appPath + '/' + instanceName + '/LOCK') as lockfile:
                    lockID = lockfile.read()
                    if lockID != jobID:
                        app_errorlogger.exception( ' - The app you want to use is currently locked! Please try again later!')
                        raise Exception('The app you want to use is currently locked! Please try again later!')
            except Exception:
                app_errorlogger.exception('Fatal error in writing to LOCK file: ', exc_info=True)
                raise Exception('Could not open LOCK file in application folder!')

        app_logger.debug( 'Locking app: ' + instanceName )
        process = subprocess.Popen(['touch' , appPath + '/' + instanceName + '/LOCK'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            app_errorlogger.error(str(output) )
        if path.exists(appPath + '/' + instanceName + '/LOCK') == False:
            app_errorlogger.exception('Something went wrong during writing LOCK file: ', exc_info=True)
            raise Exception('Fatal error in writing LOCK file: ')

    def unlock(self, jobID, instanceName, end = False):
        '''
        Description:
        -----------
        Deletes a file named LOCK to lock an app, so that one is able to perform other operations
        on an app after the current operation is finished.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        
        '''
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error(' - The folder "/application-instance" does not exist!')
        process = subprocess.Popen(['rm' , appPath + '/' + instanceName + '/LOCK'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if end == False:
            if output:
                app_errorlogger.error(str(output) )
        if path.exists(appPath + '/' + instanceName + '/LOCK') == True:
            app_errorlogger.exception('Something went wrong during deleting LOCK file: ', exc_info=True)
            raise Exception('Fatal error in deleting LOCK file: ')
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.debug('App ' + instanceName + ' unlocked')


    def downloadApp(self, jobID, instanceName,appName,version = 'master'):
        '''
        Description:
        -----------
        Downloads the wanted app from Github before installation.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        appName : str
            The (github) name of the application that is used 

        version : str
            The wanted version of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        
        '''
        if version == '' or version == None:
            version = 'master'
        bibbox_logger = AppController.setUpLog(self, jobID, 'system', systemonly=True)
        try:
            url = 'https://raw.githubusercontent.com/bibbox/application-store/master/bibboxV4.json'
            download = requests.get(url).content
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
        try:
            params = simplejson.loads(download)
        except Exception:
            bibbox_logger.exception('Error while loading bibboxV4.json file: ', exc_info=True)
            raise Exception('Error while loading bibboxV4.json file')
        appslist=[]
        
        appNameNew = 'app-'+ appName     
        rootdir = dirname(dirname(abspath(__file__)))
        print(rootdir)
        #rootdir = 'opt/bibbox/sys-bibbox'
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            raise Exception('The folder "/application-instance" does not exist!')
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Downloading app: ' + appNameNew + '/' + instanceName + ' V:' + version)
        
        process = subprocess.Popen(['git', 'clone','-b', version, 'https://github.com/bibbox/' + appNameNew + '.git', rootdir + '/application-instance/' + instanceName + '/repo/'],text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            app_logger.debug(str(output).rstrip() )
        if path.exists(appPath + '/' + instanceName + '/repo') == False:
            app_errorlogger.exception('Something went wrong during downloading app: ' + instanceName, exc_info=True)
            raise Exception('Fatal error in during downloading app: ' + instanceName)
    

    def getAppName(self, appName):
        '''
        Description:
        -----------
        Returns the repository name for the corresponding application.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        appName : str
            The (github) name of the application that is used 

        version : str
            The wanted version of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        
        '''
    
        try:
            url = 'https://raw.githubusercontent.com/bibbox/application-store/master/bibboxV4.json'
            download = requests.get(url).content
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
        try:
            params = simplejson.loads(download)
        except Exception:
            bibbox_logger.exception('Error while loading bibboxV4.json file: ', exc_info=True)
            raise Exception('Error while loading bibboxV4.json file')
        appslist=[]
        
        appName = 'app-'+appName
        sys.stdout.write(appName+ '\n')
        
        return appName


    def setInfo(self, jobID, instanceName,appName,version):
        '''
        Description:
        -----------
        Creates a file named INFO where install information is stored.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        appName : str
            The (github) name of the application that is used 

        version : str
            The wanted version of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            raise Exception('The folder "/application-instance" does not exist!')
    
        data = {}
        data['instanceName'] = instanceName
        data['appName'] = appName
        data['version'] = version
        data['jobID'] = jobID
        try:
            with open(appPath + '/' + instanceName + '/info.json', 'w+') as outfile:
                json.dump(data, outfile)
        except Exception:
                app_errorlogger.exception('Could not open file "info.json" in application folder! ', exc_info=True)
                raise Exception('Could not open file "info.json" in application folder! ')
        if path.exists(appPath + '/' + instanceName + '/info.json') == False:
            app_errorlogger.exception('Something went wrong during writing install information to info.json file of app: ' + instanceName, exc_info=True)
            raise Exception('Fatal error in during writing install information to info.json file of app: ' + instanceName)


    def changeInfo(self, jobID, instanceName, newName):
        '''
        Description:
        -----------
        Creates a file named INFO where install information is stored.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        appName : str
            The (github) name of the application that is used 

        version : str
            The wanted version of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            raise Exception('The folder "/application-instance" does not exist!')
        try:
            with open(appPath + '/' + instanceName + '/info.json') as outfile:
                data = json.load(outfile)
                data['instanceName'] = newName
                data['jobID'] = jobID
        except Exception:
                app_errorlogger.exception('Could not open file "info.json" in application folder! ', exc_info=True)
                raise Exception('Could not open file "info.json" in application folder! ')
        try:
            with open(appPath + '/' + newName + '/info.json', 'w+') as outfile:
                json.dump(data, outfile)
        except Exception:
                app_errorlogger.exception('Could not open file "info.json" in application folder! ', exc_info=True)
                raise Exception('Could not write to file "info.json" in application folder! ')


    def setProxyFiles(self, jobID, instanceName, containerName):
        '''
        Description:
        -----------
        Creates a proxy config file for the nginx web server to use the app container as sub url.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        containerName : str
            The name of the container, that is runninng the application 

        
        Raises:
        -------

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Set proxy files')
        rootdir = dirname(dirname(abspath(__file__)))
        proxyPath = rootdir + '/sys-proxy/'
        if path.exists(proxyPath) == False:
            app_errorlogger.error('The folder "sys-proxy" does not exist!')
        if path.exists(proxyPath + 'proxyconfig/sites/') == False:
            process = subprocess.Popen(['mkdir', proxyPath + 'proxyconfig/sites/'])
            output, error = process.communicate()
            if output:
                bibbox_logger.debug( str(output))
        name = instanceName + '.conf'
        
        try:
            with open(proxyPath + 'template.conf') as template:
                file_content = template.read()
                file_content = file_content.replace("§§INSTANCEID", instanceName)
                file_content = file_content.replace("§§CONTAINERNAME", containerName)
                template = open( proxyPath + 'proxyconfig/sites/' + name, 'w+')
                template.write(file_content)
                template.close()
        except Exception:
            app_errorlogger.exception('Fatal error in writing to proxy template file: ', exc_info=True)
        if path.exists(proxyPath + 'proxyconfig/sites/' + name) == False:
            app_errorlogger.exception('Something went wrong during writing the proxy file for app: ' + instanceName, exc_info=True)
            raise Exception('Fatal error in during writing the proxy file for app: ' + instanceName)
        
    def readContainernames(self, jobID, instanceName):
        '''
        Description:
        -----------
        Reads the container name from the docker-compose-template.yml file.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        ContainerNames: list
            The names of the containers, that are runninng the application
        mainContainer: str
            The name of the main container
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Read Containernames')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            raise Exception('The folder "/application-instance" does not exist!')
        composefile = open(appPath + '/' + instanceName +'/repo/docker-compose-template.yml', 'r').read()
        try:
            data = yaml.load(composefile, Loader=yaml.FullLoader)
        except Exception:
            app_errorlogger.exception('Fatal error in loading compose file: ', exc_info=True)
        ContainerNames = []
        try:
            for k, v in data["services"].items():
                if 'container_name' in v:
                    mainContainer = v.get('container_name')
                    mainContainer = mainContainer.replace('§§INSTANCE', instanceName)
                    try:
                        mainContainer = mainContainer.replace('-db', '')
                    except:
                        pass
                if 'container_name' in v:
                    ContainerName = v.get('container_name')
                    ContainerName = ContainerName.replace('§§INSTANCE', instanceName)
                    ContainerNames.append(ContainerName)
        except Exception:
            app_errorlogger.exception('Fatal error in reading compose file: ', exc_info=True)

        return ContainerNames, mainContainer

    def writeCompose(self, jobID, paramList, instanceName):
        '''
        Description:
        -----------
        Changes the instance name of the docker-compose-template.yml file.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        paramList: array
            list of environment variables that are defined in the .env file in the repository of the application

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info('Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            raise Exception('The folder "/application-instance" does not exist!')
        try:
            compose = open(appPath + '/docker-compose-template.yml', 'r').read()
        except Exception:
            app_errorlogger.exception('Fatal error in reading compose file: ', exc_info=True)

        try:
            for i, key in enumerate(paramList):
                compose = compose.replace('§§' + key, paramList[key])
        except Exception:
            app_errorlogger.exception('Fatal error in writing to compose file: ', exc_info=True)
        try:
            compose = compose.replace('§§INSTANCE', instanceName)
            target = open(appPath + '/docker-compose-template.yml', 'w')
            target.write(compose)
            target.close()
        except Exception:
            app_errorlogger.exception('Fatal error in writing to compose file: ', exc_info=True)



    def writeCLICompose(self, jobID, paramList, keyList, instanceName):
        '''
        Description:
        -----------
        Changes the instance name of the docker-compose-template.yml file.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        paramList: array
            list of environment variables that are defined in the .env file in the repository of the application

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info('Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            raise Exception('The folder "/application-instance" does not exist!')
        try:
            compose = open(appPath + '/docker-compose-template.yml', 'r').read()
        except Exception:
            app_errorlogger.exception('Fatal error in reading compose file: ', exc_info=True)
        paramList = re.sub("[^\w]", " ", paramList).split()
        
        keyList = re.sub("[^\w]", " ", keyList).split()
        
        
        for i, key in enumerate(keyList):
            if key != '':
                compose = compose.replace('§§' + key, paramList[i])
        
        
        compose = compose.replace('§§INSTANCE', instanceName)
        target = open(appPath + '/docker-compose-template.yml', 'w')
        target.write(compose)
        target.close()
        


    def composeUp(self, jobID, instanceName, containerName):
        '''
        Description:
        -----------
        Executes the doker-compose up command and starts the application

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Docker compose up')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            raise Exception('The folder "/application-instance" does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output).rstrip())
        process = subprocess.Popen(['docker', 'exec', '-it', 'local_nginx', 'service', 'nginx', 'reload'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding=sys.stdout.encoding)
        output, error = process.communicate()
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
        result = ansi_escape.sub('', output).rstrip()
        if output:
            bibbox_logger.debug( str(output).rstrip())
        process = subprocess.Popen(['docker', 'logs', containerName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.debug( str(output).rstrip())
        try:
            process = subprocess.Popen(['docker', 'exec', containerName, '/var/entrypoint.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
            output, error = process.communicate()
            if output:
                docker_logger.debug( str(output).rstrip())
        except:
            pass

    def stop(self, jobID, instanceName):
        '''
        Description:
        -----------
        Executes the doker-compose stop command to stop the application

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Stopping App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_logger.error('The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'stop'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output).rstrip())

    def start(self, jobID, instanceName):
        '''
        Description:
        -----------
        Executes the doker-compose start command to start the application

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Starting App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error( ' The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'start'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output).rstrip())

    def remove(self, jobID, instanceName):
        '''
        Description:
        -----------
        Executes the doker-compose down command to stop and remove the application

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Removing App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error( 'The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'down'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output))
        process = subprocess.Popen(['sudo', 'chmod' ,'-f', '-R', '777', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            bibbox_logger.error( str(output))
        process = subprocess.Popen(['rm' , '-f', '-R', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            bibbox_logger.error( str(output))
        process = subprocess.Popen(['rm' , '-f', rootdir + '/sys-proxy/proxyconfig/sites/' + instanceName + '.conf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            bibbox_logger.error( str(output))

    def status(self, jobID, instanceName):
        '''
        Description:
        -----------
        Reads the file STATUS to get the currend state of an application

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 
        
        Raises:
        -------

        Returns:
        -------
        status: str
            The current status of an application
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Reading Status of App: ' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/'
        if path.exists(appPath) == False:
            app_errorlogger.error( ' The folder of the app repository does not exist!')
        try:
            with open(appPath + 'STATUS') as statusfile:
                file_content = statusfile.read()
        except Exception:
            app_errorlogger.exception('Could not open STATUS file: ', exc_info=True)
        return file_content

    def checkStatus(self, jobID, instanceName, statusList):
        '''
        Description:
        -----------
        Reads the file STATUS to get the currend state of an application and checks, if the status is allowed for the wanted operation.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        statusList: array
            List of states, that allow a specific operation on an application
        
        Raises:
        -------
        raise Exception('Current app status does not allow your operation!') if the currend status is not in the statuslist

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Checking if operation is possible for current state of app: ' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/'
        if path.exists(appPath) == False:
            app_errorlogger.debug('The folder of the app repository does not exist!')
        try:
            with open(appPath + 'STATUS') as statusfile:
                file_content = statusfile.read()
                
        except Exception:
            logging.exception('Could not open STATUS file: ', exc_info=True)
        if file_content not in statusList:
            app_errorlogger.exception('Current app status does not allow operation on app: ' + instanceName)
            raise Exception('Current app status does not allow your operation!')

    def copy(self, jobID, instanceName, newName):
        '''
        Description:
        -----------
        Copies the current app folder to the new app destination.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName: str
            The instance name of the application that is used 

        newName: str
            New name of the copied application
        
        Raises:
        -------

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger,  app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info('Copy App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error('The folder of the app repository does not exist!')
        process = subprocess.Popen(['sudo', 'chmod', '-R', '777', rootdir + '/application-instance/' +  instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            app_errorlogger.error( str(output))
        process = subprocess.Popen(['cp', '-r', rootdir + '/application-instance/' + instanceName, rootdir + '/application-instance/' + newName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            app_errorlogger.error( str(output))
        

    def changeCompose(self, jobID, instanceName, newName):
        '''
        Description:
        -----------
        Reads the file STATUS to get the currend state of an application and checks, if the status is allowed for the wanted operation.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        paramList: array
            list of environment variables that are defined in the .env file in the repository of the application

        instanceName : str
            The instance name of the application that is used 

        newName: str
            new instance name name of copied application
        
        Raises:
        -------

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error(' The folder of the app repository does not exist!')
        newAppPath = rootdir + '/application-instance/' + newName + '/repo/'
        try:
            compose = open(appPath + '/docker-compose-template.yml', 'r')
        except Exception:
            app_errorlogger.exception('Fatal error in reading compose file: ', exc_info=True)
        try:
            compose = yaml.load(compose)
            services = compose['services']
        except Exception:
            app_errorlogger.exception('Fatal error in reading compose file: ', exc_info=True)
        try:
            for service in services:
                name = services[service]['container_name']
                newContainerName = name.replace(instanceName, newName)
                services[service]['container_name'] = newContainerName
                try:
                    name = services[service]['links']
                    newContainerName = name[0].replace(instanceName, newName)
                    services[service]['links'] = [newContainerName]
                except:
                    pass
                try:
                    name = services[service]['depends_on']
                    newContainerName = name[0].replace(instanceName, newName)
                    services[service]['depends_on'] = [newContainerName]
                except:
                    pass
        except Exception:
            app_errorlogger.exception('Fatal error in reading compose file: ', exc_info=True)
        try:    
            composenew = copy.deepcopy(compose)
        except Exception:
            app_errorlogger.exception('Fatal error while copying compose file: ', exc_info=True)
        try:
            for service in services:
                newServiceName = service.replace(instanceName, newName)           
                composenew['services'][newServiceName] = composenew['services'][service]
                del composenew['services'][service]
        except Exception:
            app_errorlogger.exception('Fatal error while writing to compose file: ', exc_info=True)
        try:
            composefile = yaml.dump(composenew)
            os.system('sudo chmod -R 777 ' + newAppPath)
            target = open(newAppPath + 'docker-compose-template.yml', 'w')
            target.write(composefile)
            target.close()
        except Exception:
            app_errorlogger.exception('Fatal error while writing to compose file: ', exc_info=True)

    def readVersion(self, jobID, appName):
        '''
        Description:
        -----------
        Lists the available Apps.

        Parameters:
        ----------

        Raises:
        -------

        Returns:
        -------
        appslist: json object
            The list of all available apps as json object
        '''

        try:
            url = 'https://raw.githubusercontent.com/bibbox/application-store/master/eB3Kit.json'
            download = requests.get(url).content
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
        try:
            params = simplejson.loads(download)
        except Exception:
            #app_errorlogger.exception('Error while loading eB3Kit.json file: ', exc_info=True)
            raise Exception('Error while loading eB3Kit.json file')
        versionList=[]
        try:
            for i, values in enumerate(params):
                variable = values['group_members']
                for i, var in enumerate(variable):
                    if var['app_name'] == appName:
                        versions = var['versions']
                        for version in versions:
                            versionList.append(version['docker_version'])
                    if var['app_display_name'] == appName:
                        versions = var['versions']
                        for version in versions:
                            versionList.append(version['docker_version'])
        except:
            raise Exception('The wanted app does not exist. Please check the list of available apps!')                

        return versionList

    def readAppStore(self, jobID, instanceName):
        '''
        Description:
        -----------
        Lists the available Apps.

        Parameters:
        ----------

        Raises:
        -------

        Returns:
        -------
        appslist: json object
            The list of all available apps as json object
        '''
        bibbox_logger = AppController.setUpLog(self, jobID, 'system', systemonly=True)
        try:
            url = 'https://raw.githubusercontent.com/bibbox/application-store/master/eB3Kit.json'
            download = requests.get(url).content
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
        try:
            params = simplejson.loads(download)
        except Exception:
            bibbox_logger.exception('Error while loading eB3Kit.json file: ', exc_info=True)
            raise Exception('Error while loading eB3Kit.json file')
        appslist=[]
        try:
            for i, values in enumerate(params):
                variable = values['group_members']
                for i, var in enumerate(variable):
                    appName = var['app_name']
                    if appName not in appslist:
                        appslist.append(appName)
        except Exception:
            raise Exception('Error while loading eB3Kit.json file!')
            bibbox_logger.exception('Error while loading eB3Kit.json file: ', exc_info=True)                

        return appslist
        


    def getInstalledApps(self, jobID, instanceName):
        '''
        Description:
        -----------
        Lists the available Apps.

        Parameters:
        ----------

        Raises:
        -------

        Returns:
        -------
        installedAppslist: json object
            The list of all installed apps as json object
        '''

        bibbox_logger = AppController.setUpLog(self, jobID, instanceName, systemonly=True)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' 
        if path.exists(appPath) == False:
            app_erbibbox_loggerrorlogger.error(' The folder of the app repository does not exist!')
        installedApps = {}
        try:
            for i, folder in enumerate(os.listdir(appPath)):
                try:
                    with open(appPath + '/' + folder + '/info.json') as infofile:
                        data = json.load(infofile)
                        instanceName = data['instanceName']
                        appName = data['appName']
                        installedApps[instanceName] = appName
                except:
                    pass
        except Exception:
                bibbox_logger.exception('Could not open file "info.json" in application folder! ', exc_info=True)
                raise Exception('Could not open file "info.json" in application folder! ')
                
                
        installedAppsList = json.dumps(installedApps)
        return installedAppsList

    def checkDockerState(self, jobID, instanceName, containerNames, allowedStates):
        '''
        Description:
        -----------
        Ckecks the states of all containers of an app.

        Parameters:
        ----------

        jobID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        containerNames: array
            list of used containers
        
        Raises:
        -------

        Returns:
        -------
        
        '''
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info('Checking states of all containers of app: ' + instanceName)
        states = {}
        for name in containerNames:
            process = subprocess.Popen(['docker', 'container', 'inspect', name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            try:
                params = simplejson.loads(output)
                status = params[0]['State']['Status']
                states[name] = status
            except Exception:
                app_errorlogger.exception('Could not load status of wanted container. ' + name + ' Maybe this container got removed manually. Please look at the log files!', exc_info=True)
                raise Exception('Could not load status of wanted container ' + name + ' Maybe this container got removed manually. Please look at the log files!')
            if 'all' in allowedStates:
                pass
            else:
                if status not in allowedStates:
                    app_errorlogger.error('Could not perform the wanted task. The allowed states of the app containers are: "' + ', '.join([str(elem) for elem in allowedStates]) + '". But the container of app ' + instanceName + ' has state ' + status + '.')
                    raise Exception('Could not perform the wanted task. The allowed states of the app containers are: ' + ', "'.join([str(elem) for elem in allowedStates]) + '". But the container of app ' + instanceName + ' has state ' + status + '.')

        return states

    def checkProxy(self, containerName):
        '''
        Description:
        -----------
        Ckecks the state of the proxy container.

        Parameters:
        ----------

        containerNames: array
            list of used containers
        
        Raises:
        -------

        Returns:
        -------
        
        '''
        bibbox_logger = AppController.setUpLog(self, 'system check', 'system ', systemonly=True)
        bibbox_logger.info('Performing proxy check!')
        states = {}
        process = subprocess.Popen(['docker', 'container', 'inspect', containerName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        state = ''
        try:
            params = simplejson.loads(output)
            state = params[0]['State']['Status']
        
            
            if state == 'running':
                 bibbox_logger.info('The nginx Container is running. Everything OK.')
            else:
                 bibbox_logger.error('The nginx Container is not running. Please try to restart the bibbox System with "bibbox restartSystem".')
        except:
             bibbox_logger.error('The nginx Container is not running. Please try to restart the bibbox System with "bibbox restartSystem".')

        return state

    def checkSystem(self):
        '''
        Description:
        -----------
        System Check. Checks the versions of the required packages.

        Parameters:
        ----------

        containerNames: array
            list of used containers
        
        Raises:
        -------

        Returns:
        -------
        
        '''

        bibbox_logger = AppController.setUpLog(self, 'system check', 'system ', systemonly=True)
        bibbox_logger.info('Performing system check!')

        if float(str(sys.version_info[0]) + '.' + str(sys.version_info[1])) > 3.5:
            bibbox_logger.info('Python Version: ' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + ' ---> OK!')
        else:
            bibbox_logger.error('You are using a Python version below 3.5 or do not have Python installed. Please install Python 3.5+!')
            bibbox_logger.error(output)

        process = subprocess.Popen(['docker', 'version', '--format', '{{.Server.Version}}'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        output = output.decode('utf-8')
        if version.parse(output) > version.parse("19.03.00"):
            bibbox_logger.info('Docker Version: ' + output + ' ---> OK!')
        else:
            bibbox_logger.error('You are using a Docker Engine version below 19.03.0 or do not have Docker Engine installed. Please install Docker Engine 19.03.0+!')
            bibbox_logger.error(output)

        process = subprocess.Popen(['docker-compose', 'version',  '--short'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        output = output.decode('utf8')
        
        if version.parse(str(output)) > version.parse("1.26.0"):
            bibbox_logger.info('Docker-Compose Version: ' + output + ' --->  OK!')
        else:
            bibbox_logger.error('You are using a Docker Compose version below 1.26.0 or do not have Docker Compose installed. Please install Docker Compose 1.26.0+!')
            bibbox_logger.error(output)

        process = subprocess.Popen(['docker', 'network', 'create', 'bibbox-default-network'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        output = output.decode('utf8')
        if output:
            bibbox_logger.debug('Creating default network if not already created!')

        bibbox_logger.info('Check internet connection')
        try:
            requests.get('http://216.58.192.142', timeout=1)
            bibbox_logger.debug('Internet connection ---> OK')
        except: 
            bibbox_logger.error('Can not establish an internet connection!')
            time.sleep(1)
            bibbox_logger.info('Trying to connect again.')
            try:
                requests.get('http://216.58.192.142', timeout=1)
            except:
                bibbox_logger.error('Can not connect to the internet! Please check your internet connection!')

    def checkInput(self, jobID, instanceName, inputparams):
        '''
        Description:
        -----------
        Ckecks if the userinput is valid.

        Parameters:
        ----------

        jobID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        input: array
            List of used parameters to check
        
        Raises:
        -------

        Returns:
        -------
        
        '''
        bibbox_logger = AppController.setUpLog(self, jobID, instanceName, systemonly = True)
        if type(instanceName) != str:
            bibbox_logger.debug('The input ' + instanceName + ' is not valid! Must be a string, but has type ' + type(instanceName) + '!')
        validAll = True
        if not inputparams:
            bibbox_logger.info('There are no input parameters to check')
        for var in inputparams:
            valid = bool(re.match('^[a-zA-Z0-9\-]*$',var))
            negativeList = ['admin']
            for param in negativeList:
                if param in var:
                    validAll = False
                    bibbox_logger.debug('The input ' + var + ' is not valid!')
            if valid == False:
                validAll = False
                bibbox_logger.debug('The input ' + var + ' is not valid!')

        if validAll == True:
            bibbox_logger.debug('The tested input is valid!')
        if validAll == False:
            bibbox_logger.debug('The tested input is not valid!')

        return validAll

    def checkInstall(self, jobID, instanceName, states):
        '''
        Description:
        -----------
        After the installation of an app, this function checks if the installation was sucessfull and the app is running.

        Parameters:
        ----------

        jobID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 

        states: json Object
            List of installed containers and their corresponding state
        
        Raises:
        -------

        Returns:
        -------
        
        '''
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info('Checking if installation of app ' + instanceName + ' was successful!')
        for container in states:
            state = states[container]
            if state != 'running':
                try: 
                    AppController.startApp(self, instanceName)
                except:
                    pass
            if state != 'running':
                AppController.removeApp(self, instancename)
                app_logger.error('The installation could not be completed. Please read the logs and try again')

    def startNginx(self, JobID):
        '''
        Description:
        -----------
        Starts the nginx proxy of the bibbox system.

        Parameters:
        ----------

        jobID : str
            Unique JobID that consists of an uuid and the datetime

        
        Raises:
        -------

        Returns:
        -------
        
        '''
        bibbox_logger = AppController.setUpLog(self, JobID, 'system', systemonly=True)
        bibbox_logger.info('Starting nginx container')
        
        process = subprocess.Popen(['docker-compose','-f', '/opt/bibbox/sys-bibbox/docker-compose.yml', 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            output = output.decode('utf8')
            output = output.strip()
            bibbox_logger.error(output)

    def stopNginx(self, JobID):
        '''
        Description:
        -----------
        Stops the nginx proxy of the bibbox system.

        Parameters:
        ----------

        jobID : str
            Unique JobID that consists of an uuid and the datetime

        
        Raises:
        -------

        Returns:
        -------
        
        '''
        bibbox_logger = AppController.setUpLog(self, JobID, 'system', systemonly=True)
        bibbox_logger.info('Stopping nginx container')
        
        process = subprocess.Popen(['docker-compose','-f', '/opt/bibbox/sys-bibbox/docker-compose.yml', 'down'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            output = output.decode('utf8')
            output = output.strip()
            bibbox_logger.error(output)


    


    def getParams(self, instanceName, appName, version):
        '''
        Description:
        -----------
        Reads the user parameters of an app.

        Parameters:
        ----------

        instanceName : str
            The instance name of the application that is used 

        appName: str
            Name of the wanted app

        version: str
            Version of the wanted app
        
        Raises:
        -------

        Returns:
        -------
        paramList: array
            List of all userparameters
        
        '''
        try:
            url = 'https://raw.githubusercontent.com/bibbox/' + appName + '/master/.env'
            download = requests.get(url).content
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
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

    def setParams(self, paramList):
        '''
        Description:
        -----------
        Reads the user parameters of an app.

        Parameters:
        ----------
        paramList: array
            List of all userparameters

        Raises:
        -------

        Returns:
        -------
        '''
        for key in paramList:
            paramList[key] = 'seeddms'

        return paramList


    def changeSettings(self, jobID, instanceName):
        '''
        Description:
        -----------
        Looks for config files of an app and changes them to use the app container as sub url.

        Parameters:
        ----------
        Job ID : str
            Unique JobID that consists of an uuid and the datetime

        instanceName : str
            The instance name of the application that is used 


        
        Raises:
        -------

        Returns:
        -------
        
        '''

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(self, jobID, instanceName)
        app_logger.info( 'Change setting files')
        rootdir = dirname(dirname(abspath(__file__)))
        settingsPath = rootdir + '/application-instance/' + instanceName + '/repo/config/'
        if path.exists(settingsPath) == True:
            for filename in os.listdir(settingsPath):
                try:
                    with open(settingsPath + filename) as template:
                        file_content = template.read()
                        file_content = file_content.replace("§§INSTANCENAME", instanceName)    
                        template = open( settingsPath + filename, 'w+')
                        template.write(file_content)
                        template.close()
                except:
                    pass

        entrypointPath = rootdir + '/application-instance/' + instanceName + '/repo/entrypoint.sh'

        try:
            with open(entrypointPath) as template:
                file_content = template.read()
                file_content = file_content.replace("§§INSTANCENAME", instanceName)
                template = open( entrypointPath, 'w+')
                template.write(file_content)
                template.close()
        except Exception:
            pass
        
            