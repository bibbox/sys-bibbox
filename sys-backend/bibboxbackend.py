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

class AppController:


    """
    Section: Helperfunctions
    """


    def __init__(self):
        self.rootdir = dirname(dirname(abspath(__file__)))
        self.appPath = self.rootdir + '/application-instance'
    def __del__(self):
        try:
            jobID = AppController.createJobID()
            AppController.unlock(jobID, instanceName, end = True)
        except:
            pass

    @staticmethod
    def createJobID():
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

    @staticmethod
    def checkExists(jobID, instanceName, install):
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
        bibbox_logger = AppController.setUpLog(jobID, instanceName, systemonly=True)
        appPath = rootdir + '/application-instance/'
        bibbox_logger.info('Check if app folder exists')
        if path.exists(appPath) == False:
            process = subprocess.Popen(['mkdir', appPath])
            output, error = process.communicate()
            if output:
                bibbox_logger.debug( str(output))
            #bibbox_logger.error( ' The folder "/application-instance" does not exist!')
            #raise Exception('The folder "/application-instance" does not exist')
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

    @staticmethod
    def createFolder(jobID, instanceName):
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
        bibbox_logger = AppController.setUpLog(jobID, instanceName, systemonly=True)
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

    @staticmethod
    def setup_logger(jobID, loggerName, log_file, level=logging.DEBUG):
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
        
        formatter = logging.Formatter(jobID + '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        logger = logging.getLogger(loggerName)
        if logger.handlers[:] == []:
            handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=20000000, backupCount = 10)
            handler.setFormatter(formatter)
            #if os.path.getsize(log_file) > 0:
            #    handler.doRollover()
            logger.addHandler(handler)
            logger.addHandler(logging.StreamHandler())
        logger.setLevel(level)

        return logger
    
    @staticmethod
    def setUpLog(jobID, instanceName, systemonly = False):
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
            app_logger = AppController.setup_logger(jobID, instanceName + '-app.log', logpath + 'debug.log', level=logging.DEBUG)
            app_errorlogger = AppController.setup_logger(jobID, instanceName + '-apperror.log', logpath + 'error.log', level=logging.DEBUG)
            docker_logger = AppController.setup_logger(jobID, instanceName + '-docker.log', logpath + 'docker.log', level=logging.DEBUG)
            bibbox_logger = AppController.setup_logger(jobID, instanceName + '-bibbox.log', rootdir + '/log/system.log', level=logging.DEBUG)
            
            if path.exists(logpath + 'debug.log') == False:
                raise Exception('Error while creating logfile "debug.log"')
            if path.exists(logpath + 'error.log') == False:
                raise Exception('Error while creating logfile "error.log"')
            if path.exists(logpath + 'docker.log') == False:
                raise Exception('Error while creating logfile "docker.log"')
            if path.exists(rootdir + '/log/system.log') == False:
                raise Exception('Error while creating logfile "system.log"')
            
            return app_logger, bibbox_logger, docker_logger, app_errorlogger
        else:
            bibbox_logger = AppController.setup_logger(jobID, instanceName + 'bibbox', rootdir + '/log/system.log', level=logging.DEBUG)
            if path.exists(rootdir + '/log/system.log') == False:
                raise Exception('Error while creating logfile "system.log"')
            
            return bibbox_logger

    
    @staticmethod
    def setStatus(jobID, status, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
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


    @staticmethod
    def lock(jobID, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
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

    @staticmethod
    def unlock(jobID, instanceName, end = False):
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
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.debug('Unlocking app: ' + instanceName )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error(' - The folder "/application-instance" does not exist!')
        process = subprocess.Popen(['rm' , appPath + '/' + instanceName + '/LOCK'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if end == False:
            output, error = process.communicate()
            if output:
                app_errorlogger.error(str(output) )
        if path.exists(appPath + '/' + instanceName + '/LOCK') == True:
            app_errorlogger.exception('Something went wrong during deleting LOCK file: ', exc_info=True)
            raise Exception('Fatal error in deleting LOCK file: ')


    @staticmethod
    def downloadApp(jobID, instanceName,appName,version):
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
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error(' - The folder "/application-instance" does not exist!')
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Downloading app: ' + appName + '/' + instanceName + ' V:' + version)
        
        process = subprocess.Popen(['git', 'clone','-b', version, 'https://github.com/bibbox/' + appName + '.git', 'application-instance/' + instanceName + '/repo/'],text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #output = process.stdout.readline()
        output, error = process.communicate()
        if output:
            app_logger.debug(str(output).rstrip() )
        if path.exists(appPath + '/' + instanceName + '/repo') == False:
            app_errorlogger.exception('Something went wrong during downloading app: ' + instanceName, exc_info=True)
            raise Exception('Fatal error in during downloading app: ' + instanceName)
    
    @staticmethod
    def setInfo(jobID, instanceName,appName,version):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error('The folder "/application-instance" does not exist!')
        #try:
        #    text_file = open(appPath + '/' + instanceName + '/INFO.json', "w")
        #    text_file.write(jobID + '\n' + appName + '\n' + instanceName + '\n' + version)
        #    text_file.close()
        #except Exception:
        #    app_logger.exception('Fatal error in writing to INFO file: ', exc_info=True)

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


    @staticmethod
    def changeInfo(jobID, instanceName, newName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error('The folder "/application-instance" does not exist!')
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


    @staticmethod
    def setProxyFiles(jobID, instanceName, containerName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
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
                file_content = file_content.replace("§§INSTANCEID", instanceName + '/')
                file_content = file_content.replace("§§CONTAINERNAME", containerName + '/')
                template = open( proxyPath + 'proxyconfig/sites/' + name, 'w+')
                template.write(file_content)
                template.close()
        except Exception:
            app_errorlogger.exception('Fatal error in writing to proxy template file: ', exc_info=True)
        if path.exists(proxyPath + 'proxyconfig/sites/' + name) == False:
            app_errorlogger.exception('Something went wrong during writing the proxy file for app: ' + instanceName, exc_info=True)
            raise Exception('Fatal error in during writing the proxy file for app: ' + instanceName)
        
    @staticmethod
    def readContainernames(jobID, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Read Containernames')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            app_errorlogger.error(' The folder "/application-instance" does not exist!')
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

    @staticmethod
    def writeCompose(jobID, paramList, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info('Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error(' The folder "/application-instance" does not exist!')
        try:
            compose = open(appPath + '/docker-compose-template.yml', 'r').read()
        except Exception:
            app_errorlogger.exception('Fatal error in reading compose file: ', exc_info=True)

        #compose = yaml.load(compose)
        try:
            for key in paramList:
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
    @staticmethod
    def composeUp(jobID, instanceName, containerName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Docker compose up')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_logger.error( 'The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output).rstrip())
        process = subprocess.Popen(['docker', 'exec', '-it', 'local_nginx', 'service', 'nginx', 'reload'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding=sys.stdout.encoding)
        output, error = process.communicate()
        #ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]|\[0-9][.])')
        #result = ansi_escape.sub('', output)
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
        #result = result.replace('m.','').replace('[','')
        if output:
            bibbox_logger.debug( str(output).rstrip())
        process = subprocess.Popen(['docker', 'logs', containerName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output).rstrip())

    @staticmethod
    def stop(jobID, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Stopping App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_logger.error('The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'stop'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output).rstrip())
        #os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml stop ')

    @staticmethod
    def start(jobID, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Starting App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error( ' The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'start'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output).rstrip())
        #os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml start ')

    @staticmethod
    def remove(jobID, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Romoving App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error( 'The folder of the app repository does not exist!')
        #os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml down ')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'down'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output))
        process = subprocess.Popen(['sudo', 'chmod' ,'-f', '-R', '777', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            docker_logger.error( str(output))
        process = subprocess.Popen(['rm' , '-f', '-R', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            bibbox_logger.error( str(output))
        process = subprocess.Popen(['rm' , '-f', rootdir + '/sys-proxy/proxyconfig/sites/' + instanceName + '.conf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            bibbox_logger.error( str(output))

    @staticmethod
    def status(jobID, instanceName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
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

    @staticmethod
    def checkStatus(jobID, instanceName, statusList):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info( 'Checking if operation is possible for current state of app: ' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/'
        if path.exists(appPath) == False:
            app_errorlogger.debug('The folder of the app repository does not exist!')
        try:
            with open(appPath + 'STATUS') as statusfile:
                file_content = statusfile.read()
                #try:
                #    file_content.replace('\n', '')
                #except:
                #    pass
        except Exception:
            logging.exception('Could not open STATUS file: ', exc_info=True)
        if file_content not in statusList:
            app_errorlogger.exception('Current app status does not allow operation on app: ' + instanceName)
            raise Exception('Current app status does not allow your operation!')

    @staticmethod
    def copy(jobID, instanceName, newName):
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

        app_logger, bibbox_logger, docker_logger,  app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info('Copy App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            app_errorlogger.error('The folder of the app repository does not exist!')
        #process = subprocess.Popen(['sudo', 'cp', '-r', rootdir + '/application-instance/' + instanceName, rootdir + '/application-instance/' + newName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process = subprocess.Popen(['cp', '-r', rootdir + '/application-instance/' + instanceName, rootdir + '/application-instance/' + newName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output, error = process.communicate()
        if output:
            app_errorlogger.error( str(output))

    @staticmethod
    def changeCompose(jobID, instanceName, newName):
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

        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
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

    @staticmethod
    def readVersion(jobID, appName):
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

        #app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
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

    @staticmethod
    def readAppStore(jobID, instanceName):
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
        bibbox_logger = AppController.setUpLog(jobID, instanceName, systemonly=True)
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
        


    @staticmethod
    def getInstalledApps(jobID, instanceName):
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

        bibbox_logger = AppController.setUpLog(jobID, instanceName, systemonly=True)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' 
        if path.exists(appPath) == False:
            app_erbibbox_loggerrorlogger.error(' The folder of the app repository does not exist!')
        installedApps = {}
        try:
            for i, folder in enumerate(os.listdir(appPath)):
                with open(appPath + '/' + folder + '/info.json') as infofile:
                    data = json.load(infofile)
                    instanceName = data['instanceName']
                    appName = data['appName']
        except Exception:
                bibbox_logger.exception('Could not open file "info.json" in application folder! ', exc_info=True)
                raise Exception('Could not open file "info.json" in application folder! ')
                
                installedApps[instanceName] = appName
        installedAppsList = json.dumps(installedApps)
        return installedAppsList

    @staticmethod
    def checkDockerState(jobID, instanceName, containerNames, allowedStates):
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
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        app_logger.info('Checking states of all containers of app: ' + instanceName)
        states = {}
        for name in containerNames:
            process = subprocess.Popen(['docker', 'container', 'inspect', name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            #if output:
            #    app_errorlogger.error( str(output))
            try:
                params = simplejson.loads(output)
                status = params[0]['State']['Status']
                states[name] = status
            except Exception:
                app_errorlogger.exception('Could not load status of wanted container ' + name, exc_info=True)
                raise Exception('Could not load ststus of wanted container ' + name)
            if 'all' in allowedStates:
                pass
            else:
                if status not in allowedStates:
                    app_errorlogger.error('The allowed states of the app containers are ' + ', '.join([str(elem) for elem in allowedStates]) + ', but the container of app ' + instanceName + ' has state ' + status)
                    raise Exception('The allowed states of the app containers are ' + ', '.join([str(elem) for elem in allowedStates]) + ', but the container of app ' + instanceName + ' has state ' + status)
            #except:
            #    output = output.decode('ascii').rstrip('\n')
            #    app_logger.debug( str(output))

        return states

    @staticmethod
    def checkInput(jobID, instanceName, inputparams):
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
        app_logger, bibbox_logger, docker_logger, app_errorlogger = AppController.setUpLog(jobID, instanceName)
        validAll = True
        if not inputparams:
            app_logger.info('There are no input parameters to check')
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


    """
    Section: Main functions
    """

    @staticmethod
    def getParams(instanceName, appName, version):
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

    @staticmethod
    def setParams(paramList):
        #data = json.load(paramList)
        for key in paramList:
            paramList[key] = 'seeddms'

        return paramList

    
    @staticmethod
    def installApp(paramList, instanceName, appName, version):
        '''
        Description:
        -----------
        Installs a new bibbox app with a specific unique name.

        Parameters:
        ----------

        paramList: array
            list of environment variables that are defined in the .env file in the repository of the application

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
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install = True)
        AppController.createFolder(jobID, instanceName)
        inputparams = [instanceName, appName, version]
        AppController.checkInput(jobID, instanceName, inputparams)
        AppController.setStatus(jobID, 'Prepare Install', instanceName)
        #AppController.setUpLog(jobID, instanceName)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Downloading', instanceName)
        AppController.downloadApp(jobID, instanceName,appName,version)
        AppController.setStatus(jobID, 'Installing', instanceName)
        AppController.setInfo(jobID, instanceName,appName,version)
        containerNames, mainContainer = AppController.readContainernames(jobID, instanceName)
        AppController.setProxyFiles(jobID, instanceName, mainContainer)
        AppController.writeCompose(jobID, paramList, instanceName)
        AppController.composeUp(jobID, instanceName, mainContainer)
        AppController.unlock(jobID, instanceName)
        AppController.checkDockerState(jobID, instanceName, containerNames, ['running'])
        AppController.setStatus(jobID, 'Running', instanceName)
    
    @staticmethod
    def stopApp(instanceName):
        '''
        Description:
        -----------
        Stops the wanted app.

        Parameters:
        ----------

        instanceName : str
            The instance name of the application that is used 

        Raises:
        -------

        Returns:
        -------
        
        '''
        #statusList = ['Running']
        jobID = AppController.createJobID()
        #AppController.setUpLog(jobID, instanceName, systemonly=True)
        AppController.checkExists(jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(jobID, instanceName, inputparams)
        containerNames, mainContainer = AppController.readContainernames(jobID, instanceName)
        AppController.checkDockerState(jobID, instanceName, containerNames, ['running'])
        #AppController.checkStatus(jobID, instanceName, statusList)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Stopping', instanceName)
        #AppController.setUpLog(jobID, instanceName)
        AppController.stop(jobID, instanceName)
        AppController.unlock(jobID, instanceName)
        AppController.checkDockerState(jobID, instanceName, containerNames, ['paused', 'stopped', 'exited'])
        AppController.setStatus(jobID, 'Stopped', instanceName)



    @staticmethod
    def startApp(instanceName):
        '''
        Description:
        -----------
        Starts the wanted app.

        Parameters:
        ----------

        instanceName : str
            The instance name of the application that is used 

        Raises:
        -------

        Returns:
        -------
        
        '''
        #statusList = ['Stopped']
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(jobID, instanceName, inputparams)
        #AppController.checkStatus(jobID, instanceName, statusList)
        containerNames, mainContainer = AppController.readContainernames(jobID, instanceName)
        AppController.checkDockerState(jobID, instanceName, containerNames, ['paused', 'stopped', 'exited'])
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Starting', instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.start(jobID, instanceName)
        AppController.unlock(jobID, instanceName)
        AppController.checkDockerState(jobID, instanceName, containerNames, ['running'])
        AppController.setStatus(jobID, 'Running', instanceName)

    @staticmethod
    def removeApp(instanceName):
        '''
        Description:
        -----------
        Removes the wanted app.

        Parameters:
        ----------

        instanceName : str
            The instance name of the application that is used 

        Raises:
        -------

        Returns:
        -------
        
        '''
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(jobID, instanceName, inputparams)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Removing App', instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.remove(jobID, instanceName)

    @staticmethod
    def getStatus(instanceName):
        '''
        Description:
        -----------
        Returns status of a specific application.

        Parameters:
        ----------

        instanceName : str
            The instance name of the application that is used 

        Raises:
        -------

        Returns:
        -------
        
        '''
        jobID = AppController.createJobID()
        containerNames, mainContainer = AppController.readContainernames(jobID, instanceName)
        AppController.checkExists(jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(jobID, instanceName, inputparams)
        AppController.setUpLog(jobID, instanceName)
        #AppController.status(jobID, instanceName)
        allowedStates = ['all']
        states = AppController.checkDockerState(jobID, instanceName, containerNames, allowedStates)
        return states

    @staticmethod
    def copyApp(instanceName, newName):
        '''
        Description:
        -----------
        Copies the wanted app with a new name.

        Parameters:
        ----------

        instanceName : str
            The instance name of the application that is used 

        newName : str
            The new name of the application that is used 

        Raises:
        -------

        Returns:
        -------
        
        '''
        jobID = AppController.createJobID()
        AppController.checkExists(jobID, instanceName, install=False)
        inputparams = [instanceName, newName]
        AppController.checkInput(jobID, instanceName, inputparams)
        AppController.lock(jobID, instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.copy(jobID, instanceName, newName)
        AppController.setUpLog(jobID, newName)
        AppController.changeCompose(jobID, instanceName, newName)
        AppController.unlock(jobID, instanceName)
        ContainerNames, mainContainer = AppController.readContainernames(jobID, newName)
        AppController.setProxyFiles(jobID, newName, mainContainer)
        AppController.changeInfo(jobID, instanceName, newName)
        AppController.composeUp(jobID, newName, mainContainer)
        AppController.unlock(jobID, newName)
        AppController.setStatus(jobID, 'Running', instanceName)

        
    @staticmethod
    def listApps():

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
        jobID = AppController.createJobID()
        instanceName = 'system'
        appsList = AppController.readAppStore(jobID, instanceName)
        return appsList

    @staticmethod
    def listInstalledApps():

        '''
        Description:
        -----------
        Lists all installed Apps.

        Parameters:
        ----------

        Raises:
        -------

        Returns:
        -------
        appslist: json object
            The list of all available apps as json object
        '''
        jobID = AppController.createJobID()
        instanceName = 'system'
        installedAppsList = AppController.getInstalledApps(jobID, instanceName)
        return installedAppsList



