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
import copy
from os import path
from subprocess import check_output
import simplejson

class AppController:


    """
    Section: Helperfunctions
    """


    def __init__(self):
        self.rootdir = dirname(dirname(abspath(__file__)))
        self.appPath = self.rootdir + '/application-instance'

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
            Unique JobID that consists of an uuid and the datetime
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
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            raise Exception('The application instance path does not exist')
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
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        subprocess.Popen(['mkdir' , appPath + '/' + instanceName])
        subprocess.Popen(['touch' , appPath + '/' + instanceName + '/app.log'])

    @staticmethod
    def setUpLog(jobID, instanceName):
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
        appPath = rootdir + '/application-instance'
        path = appPath + '/' + instanceName + '/'
        try:
            logging.basicConfig(filename= path + 'app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
            
        except Exception:
            print(Exception)


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
        logging.info(jobID + ' - ' + 'Set status to ' + status )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder "/application-instance" does not exist!')
        process = subprocess.Popen(['touch' , appPath + '/' + instanceName + '/STATUS'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        try:
            text_file = open(appPath + '/' + instanceName + '/STATUS', "w")
            text_file.write(status)
            text_file.close()
        except Exception:
            logging.exception('Fatal error in writing to STATUS file: ', exc_info=True)

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
        logging.info(jobID + ' - ' + 'Ckeck if app is locked' )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder "/application-instance" does not exist!')
        if 'LOCK' in os.listdir(appPath + '/' + instanceName):
            try:
                with open(appPath + '/' + instanceName + '/LOCK') as lockfile:
                    lockID = lockfile.read()
                    if lockID != jobID:
                        logging.exception( jobID + ' - The app you want to use is currently locked! Please try again later!')
                        raise Exception('The app you want to use is currently locked! Please try again later!')
            except Exception:
                logging.exception('Fatal error in writing to LOCK file: ', exc_info=True)

        logging.debug(jobID + ' - ' + 'Locking app: ' + instanceName )
        process = subprocess.Popen(['touch' , appPath + '/' + instanceName + '/LOCK'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output) )
    
    @staticmethod
    def unlock(jobID, instanceName):
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
        logging.debug(jobID + ' - ' + 'Unlocking app: ' + instanceName )
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder "/application-instance" does not exist!')
        process = subprocess.Popen(['rm' , appPath + '/' + instanceName + '/LOCK'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output) )

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
        logging.info(jobID + ' - ' + 'Downloading app: ' + appName + '/' + instanceName + ' V:' + version)
        
        process = subprocess.Popen(['git', 'clone','-b', version, 'https://github.com/bibbox/' + appName + '.git', 'application-instance/' + instanceName + '/repo/'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if output:
            logging.exception(jobID + str(output) )
    
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
        logging.info(jobID + ' - ' + 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder "/application-instance" does not exist!')
        #try:
        #    text_file = open(appPath + '/' + instanceName + '/INFO.json', "w")
        #    text_file.write(jobID + '\n' + appName + '\n' + instanceName + '\n' + version)
        #    text_file.close()
        #except Exception:
        #    logging.exception('Fatal error in writing to INFO file: ', exc_info=True)

        data = {}
        data['instanceName'] = instanceName
        data['appName'] = appName
        data['version'] = version
        data['jobID'] = jobID

        with open(appPath + '/' + instanceName + '/info.json', 'w+') as outfile:
            json.dump(data, outfile)

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
        logging.info(jobID + ' - ' + 'Set install info')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder "/application-instance" does not exist!')
        #try:
        #    text_file = open(appPath + '/' + instanceName + '/INFO.json', "w")
        #    text_file.write(jobID + '\n' + appName + '\n' + instanceName + '\n' + version)
        #    text_file.close()
        #except Exception:
        #    logging.exception('Fatal error in writing to INFO file: ', exc_info=True)

        with open(appPath + '/' + instanceName + '/info.json') as outfile:
            data = json.load(outfile)
            data['instanceName'] = newName
            data['jobID'] = jobID
        with open(appPath + '/' + newName + '/info.json', 'w+') as outfile:
            json.dump(data, outfile)

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
        logging.info(jobID + ' - ' + 'Set proxy files')
        rootdir = dirname(dirname(abspath(__file__)))
        proxyPath = rootdir + '/sys-proxy/'
        if path.exists(proxyPath) == False:
            logging.debug(jobID + ' - The folder "sys-proxy" does not exist!')
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
            logging.exception('Fatal error in writing to proxy template file: ', exc_info=True)
        
    @staticmethod
    def readContainername(jobID, instanceName):
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
        ContainerName: str
            The name of the container, that is runninng the application
        '''
        logging.info(jobID + ' - ' + 'Read Containername')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder "/application-instance" does not exist!')
        composefile = open(appPath + '/' + instanceName +'/repo/docker-compose-template.yml', 'r').read()
        try:
            data = yaml.load(composefile)
        except Exception:
            logging.exception('Fatal error in loading compose file: ', exc_info=True)
        try:
            for k, v in data["services"].items():
                if 'container_name' in v:
                    ContainerName = v.get('container_name')
                    ContainerName = ContainerName.replace('§§INSTANCE', instanceName)
                    try:
                        ContainerName = ContainerName.replace('-db', '')
                    except:
                        pass
        except Exception:
            logging.exception('Fatal error in reading compose file: ', exc_info=True)

        return ContainerName

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
        logging.info(jobID + ' - ' + 'Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder "/application-instance" does not exist!')
        try:
            compose = open(appPath + '/docker-compose-template.yml', 'r').read()
        except Exception:
            logging.exception('Fatal error in reading compose file: ', exc_info=True)

        #compose = yaml.load(compose)
        try:
            for key in paramList:
                compose = compose.replace('§§' + key, paramList[key])
        except Exception:
            logging.exception('Fatal error in writing to compose file: ', exc_info=True)
        try:
            compose = compose.replace('§§INSTANCE', instanceName)
            target = open(appPath + '/docker-compose-template.yml', 'w')
            target.write(compose)
            target.close()
        except Exception:
            logging.exception('Fatal error in writing to compose file: ', exc_info=True)
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
        logging.info(jobID + ' - ' + 'Docker compose up')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'up', '-d'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['docker', 'exec', '-it', 'local_nginx', 'service', 'nginx', 'reload'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['docker', 'logs', containerName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))

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
        logging.info(jobID + ' - ' + 'Stopping App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'stop'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
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
        logging.info(jobID + ' - ' + 'Starting App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'start'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
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
        logging.info(jobID + ' - ' + 'Romoving App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
        #os.system('docker-compose -f ' + appPath + '/docker-compose-template.yml down ')
        process = subprocess.Popen(['docker-compose', '-f', appPath + '/docker-compose-template.yml', 'down'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['sudo', 'chmod' ,'-f', '-R', '777', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['rm' , '-f', '-R', rootdir + '/application-instance/' + instanceName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))
        process = subprocess.Popen(['rm' , '-f', rootdir + '/sys-proxy/proxyconfig/sites/' + instanceName + '.conf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))

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
        logging.info(jobID + ' - ' + 'Reading Status of App: ' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
        try:
            with open(appPath + 'STATUS') as statusfile:
                file_content = statusfile.read()
        except Exception:
            logging.exception('Could not open STATUS file: ', exc_info=True)
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
        logging.info(jobID + ' - ' + 'Checking if operation is possible for current state of app: ' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
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
            logging.exception(jobID + ' - ' + 'Current app status does not allow operation on app: ' + instanceName)
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
        logging.info(jobID + ' - ' + 'Copy App:' + instanceName)
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
        #process = subprocess.Popen(['sudo', 'cp', '-r', rootdir + '/application-instance/' + instanceName, rootdir + '/application-instance/' + newName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process = subprocess.Popen(['cp', '-r', rootdir + '/application-instance/' + instanceName, rootdir + '/application-instance/' + newName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output, error = process.communicate()
        if output:
            logging.debug(jobID + str(output))

    @staticmethod
    def changeCompose(jobID, paramList, instanceName, newName):
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
        logging.info(jobID + ' - ' + 'Write parameters to compose file')
        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' + instanceName + '/repo/'
        if path.exists(appPath) == False:
            logging.debug(jobID + ' - The folder of the app repository does not exist!')
        newAppPath = rootdir + '/application-instance/' + newName + '/repo/'
        try:
            compose = open(appPath + '/docker-compose-template.yml', 'r')
        except Exception:
            logging.exception('Fatal error in reading compose file: ', exc_info=True)
        try:
            compose = yaml.load(compose)
            services = compose['services']
        except Exception:
            logging.exception('Fatal error in reading compose file: ', exc_info=True)
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
            logging.exception('Fatal error in reading compose file: ', exc_info=True)
        try:    
            composenew = copy.deepcopy(compose)
        except Exception:
            logging.exception('Fatal error while copying compose file: ', exc_info=True)
        try:
            for service in services:
                newServiceName = service.replace(instanceName, newName)           
                composenew['services'][newServiceName] = composenew['services'][service]
                del composenew['services'][service]
        except Exception:
            logging.exception('Fatal error while writing to compose file: ', exc_info=True)
        try:
            composefile = yaml.dump(composenew)
            os.system('sudo chmod -R 777 ' + newAppPath)
            target = open(newAppPath + 'docker-compose-template.yml', 'w')
            target.write(composefile)
            target.close()
        except Exception:
            logging.exception('Fatal error while writing to compose file: ', exc_info=True)

    @staticmethod
    def readAppStore():
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
            url = 'https://raw.githubusercontent.com/bibbox/application-store/master/applications.json'
        except Exception:
            raise Exception('Something went wrong during connecting to the GitHub repository. Please Check your internet connection!')
        download = requests.get(url).content
        try:
            params = simplejson.loads(download)
        except Exception:
            logging.exception('Error while loading applications.json file: ', exc_info=True)
        apps=[]
        gitNames=[]
        for i, values in enumerate(params):
            try:
                apps.append(values['name'])
                gitNames.append(values['github_name'])
            except Exception:
                logging.exception('Error while reading applications.json file: ', exc_info=True)
        appsList = json.dumps(apps)
        return appsList
        


    @staticmethod
    def getInstalledApps():
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
            The list of all installed apps as json object
        '''

        rootdir = dirname(dirname(abspath(__file__)))
        appPath = rootdir + '/application-instance/' 
        installedApps = {}
        for i, folder in enumerate(os.listdir(appPath)):
            with open(appPath + '/' + folder + '/info.json') as infofile:
                data = json.load(infofile)
                instanceName = data['instanceName']
                appName = data['appName']
                
                installedApps[instanceName] = appName
        installedAppsList = json.dumps(installedApps)
        return installedAppsList



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
        AppController.setStatus(jobID, 'Prepare Install', instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.lock(jobID, instanceName)
        AppController.setStatus(jobID, 'Downloading', instanceName)
        AppController.downloadApp(jobID, instanceName,appName,version)
        AppController.setStatus(jobID, 'Installing', instanceName)
        AppController.setInfo(jobID, instanceName,appName,version)
        containerName = AppController.readContainername(jobID, instanceName)
        AppController.setProxyFiles(jobID, instanceName, containerName)
        AppController.writeCompose(jobID, paramList, instanceName)
        AppController.composeUp(jobID, instanceName, containerName)
        AppController.unlock(jobID, instanceName)
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
        AppController.checkExists(jobID, instanceName, install=False)
        AppController.setUpLog(jobID, instanceName)
        AppController.status(jobID, instanceName)

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
        AppController.lock(jobID, instanceName)
        AppController.setUpLog(jobID, instanceName)
        AppController.copy(jobID, instanceName, newName)
        AppController.setUpLog(jobID, newName)
        AppController.changeCompose(jobID, paramList, instanceName, newName)
        AppController.unlock(jobID, instanceName)
        containerName = AppController.readContainername(jobID, newName)
        AppController.setProxyFiles(jobID, newName, containerName)
        AppController.changeInfo(jobID, instanceName, newName)
        AppController.composeUp(jobID, newName, containerName)
        AppController.unlock(jobID, instanceName)
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
        appsList = AppController.readAppStore()
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
        
        installedAppsList = AppController.getInstalledApps()
        return installedAppsList



x = AppController()
paramList, instanceName, appName, version = x.getParams('seeddmsproxytest','app-seeddmsTNG','master')
paramList = x.setParams(paramList)

#x.installApp(paramList, instanceName, appName, version)
#status = x.getStatus(instanceName)
#x.stopApp(instanceName) 
#x.startApp(instanceName)
#x.removeApp(instanceName)
#x.copyApp('seeddmsproxytest', 'testappnew')
appsList = x.listInstalledApps()
pass