#!/usr/bin/env python3

from helperFunctions import AppController
import subprocess


__author__ = "Stefan Herdy"
__credits__ = ["Heimo Müller", "Robert Reihs ", "Markus Plass",]
__license__ = "..."
__version__ = "1.0.1"
__email__ = "stefan.herdy@medunigraz.at"
__status__ = "Development"


class MainFunctions(AppController):
    def __init__(self):
        super().__init__()

        process = subprocess.Popen(['docker network ls|grep bibbox-default-network > /dev/null || docker network create  bibbox-default-network'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        #states = AppController.checkDockerState(self, jobID, instanceName, 'local_nginx', ['running'])


    def __del__(self):
        try:
            jobID = AppController.createJobID(self)
            instanceName = self.instanceName
            AppController.unlock(self, jobID, instanceName, end = True)
        except:
            pass
    
#    @staticmethod
    def installApp(self, paramList, keyList, instanceName, appName, version, CLI=False):
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
        self.instanceName = instanceName
        jobID = AppController.createJobID(self)
        AppController.checkExists(self, jobID, instanceName, install = True)
        inputparams = [instanceName, appName, version]
        AppController.checkInput(self, jobID, instanceName, inputparams)
        AppController.createFolder(self, jobID, instanceName)
        AppController.setStatus(self, jobID, 'Prepare Install', instanceName)
        AppController.setUpLog(self, jobID, instanceName)
        AppController.lock(self, jobID, instanceName)
        AppController.setStatus(self, jobID, 'Downloading', instanceName)
        AppController.downloadApp(self, jobID, instanceName,appName,version)
        AppController.setStatus(self, jobID, 'Installing', instanceName)
        AppController.setInfo(self, jobID, instanceName,appName,version)
        containerNames, mainContainer = AppController.readContainernames(self, jobID, instanceName)
        AppController.setProxyFiles(self, jobID, instanceName, mainContainer)
        AppController.changeSettings(self, jobID, instanceName)
        if CLI == True:
            AppController.writeCLICompose(self, jobID, paramList, keyList, instanceName)
        else:
            AppController.writeCompose(self, jobID, paramList, instanceName)
        AppController.composeUp(self, jobID, instanceName, mainContainer)
        AppController.unlock(self, jobID, instanceName)
        states = AppController.checkDockerState(self, jobID, instanceName, containerNames, ['running'])
        AppController.checkInstall(self, instanceName, states)
        AppController.setStatus(self, jobID, 'Running', instanceName)
        AppController.stopNginx(self, jobID)
        AppController.startNginx(self, jobID)

    


    def stopApp(self, instanceName):
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
        jobID = AppController.createJobID(self, )
        #AppController.setUpLog(jobID, instanceName, systemonly=True)
        AppController.checkExists(self, jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(self, jobID, instanceName, inputparams)
        containerNames, mainContainer = AppController.readContainernames(self, jobID, instanceName)
        AppController.checkDockerState(self, jobID, instanceName, containerNames, ['running'])
        #AppController.checkStatus(jobID, instanceName, statusList)
        AppController.lock(self, jobID, instanceName)
        AppController.setStatus(self, jobID, 'Stopping', instanceName)
        #AppController.setUpLog(jobID, instanceName)
        AppController.stop(self, jobID, instanceName)
        AppController.unlock(self, jobID, instanceName)
        AppController.checkDockerState(self, jobID, instanceName, containerNames, ['paused', 'stopped', 'exited'])
        AppController.setStatus(self, jobID, 'Stopped', instanceName)



 #   @staticmethod
    def startApp(self, instanceName):
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
        jobID = AppController.createJobID(self, )
        AppController.checkExists(self, jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(self, jobID, instanceName, inputparams)
        #AppController.checkStatus(jobID, instanceName, statusList)
        containerNames, mainContainer = AppController.readContainernames(self, jobID, instanceName)
        AppController.checkDockerState(self, jobID, instanceName, containerNames, ['paused', 'stopped', 'exited'])
        AppController.lock(self, jobID, instanceName)
        AppController.setStatus(self, jobID, 'Starting', instanceName)
        AppController.setUpLog(self, jobID, instanceName)
        AppController.start(self, jobID, instanceName)
        AppController.unlock(self, jobID, instanceName)
        AppController.checkDockerState(self, jobID, instanceName, containerNames, ['running'])
        AppController.setStatus(self, jobID, 'Running', instanceName)

 #   @staticmethod
    def removeApp(self, instanceName):
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
        jobID = AppController.createJobID(self)
        AppController.checkExists(self, jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(self, jobID, instanceName, inputparams)
        AppController.lock(self, jobID, instanceName)
        AppController.setStatus(self, jobID, 'Removing App', instanceName)
        #AppController.setUpLog(jobID, instanceName, systemonly=True)
        AppController.remove(self, jobID, instanceName)

 #   @staticmethod
    def getStatus(self, instanceName):
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
        status : str
            The current status of the application that is used 
        
        '''
        jobID = AppController.createJobID(self)
        containerNames, mainContainer = AppController.readContainernames(self, jobID, instanceName)
        AppController.checkExists(self, jobID, instanceName, install=False)
        inputparams = [instanceName]
        AppController.checkInput(self, jobID, instanceName, inputparams)
        AppController.setUpLog(self, jobID, instanceName)
        #AppController.status(jobID, instanceName)
        allowedStates = ['all']
        states = AppController.checkDockerState(self, jobID, instanceName, containerNames, allowedStates)
        return states

 #   @staticmethod
    def copyApp(self, instanceName, newName):
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
        jobID = AppController.createJobID(self, )
        AppController.checkExists(self, jobID, instanceName, install=False)
        AppController.checkExists(self, jobID, newName, install=True)
        inputparams = [instanceName, newName]
        AppController.checkInput(self, jobID, instanceName, inputparams)
        AppController.lock(self, jobID, instanceName)
        AppController.setUpLog(self, jobID, instanceName)
        AppController.copy(self, jobID, instanceName, newName)
        AppController.setUpLog(self, jobID, newName)
        AppController.changeCompose(self, jobID, instanceName, newName)
        AppController.unlock(self, jobID, instanceName)
        ContainerNames, mainContainer = AppController.readContainernames(self, jobID, newName)
        AppController.setProxyFiles(self, jobID, newName, mainContainer)
        AppController.changeInfo(self, jobID, instanceName, newName)
        AppController.composeUp(self, jobID, newName, mainContainer)
        AppController.unlock(self, jobID, newName)
        AppController.setStatus(self, jobID, 'Running', instanceName)

        
 #   @staticmethod
    def listApps(self):

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
        jobID = AppController.createJobID(self)
        instanceName = 'system'
        appsList = AppController.readAppStore(self, jobID, instanceName)
        print(appsList)
        return appsList
        

 #   @staticmethod
    def listInstalledApps(self):

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
        jobID = AppController.createJobID(self)
        instanceName = 'system'
        installedAppsList = AppController.getInstalledApps(self, jobID, instanceName)
        return installedAppsList


 #   @staticmethod
    def startBibbox(self):

        '''
        Description:
        -----------
        Starts the BiBBoX System.

        Parameters:
        ----------

        Raises:
        -------

        Returns:
        -------
        
        '''
        jobID = AppController.createJobID(self)
        AppController.startNginx(self, jobID)

 #   @staticmethod
    def stopBibbox(self):

        '''
        Description:
        -----------
        Starts the BiBBoX System.

        Parameters:
        ----------

        Raises:
        -------

        Returns:
        -------
        
        '''
        jobID = AppController.createJobID(self)
        AppController.stopNginx(self, jobID)

    def restartBibbox(self):
        '''
        Description:
        -----------
        Restarts the BiBBoX System.

        Parameters:
        ----------

        Raises:
        -------

        Returns:
        -------
        
        '''
        jobID = AppController.createJobID(self)
        AppController.stopNginx(self, jobID)
        AppController.startNginx(self, jobID)



