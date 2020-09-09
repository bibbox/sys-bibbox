#!/usr/bin/env python3

import os
import json
import yaml
import subprocess
from os.path import dirname, abspath
import traceback



class AppController:

    def __init__(self, instanceName, *args, **kwargs):
        
        self.instanceName = instanceName
        self.rootdir = dirname(dirname(abspath(__file__)))
        self.appPath = self.rootdir + '/application-instance'
        self.exists = False
        
        for key, value in kwargs.items():
            if key == 'version':
                self.version = value
            if key == 'appName':
                self.appName = value

        #subprocess.Popen(['touch' , self.appPath + '/' + self.instanceName + '/LOCK'])

        if instanceName in os.listdir(self.appPath):
            self.exists = True
            if 'LOCK' in os.listdir(self.appPath + '/' + self.instanceName):
                self.locked = True
                #raise Exception('The app you want to stop does not exist!')
        
            subprocess.Popen(['touch' , self.appPath + '/' + self.instanceName + '/LOCK'])


    def __del__(self):
        subprocess.Popen(['rm' , self.appPath + '/' + self.instanceName + '/LOCK'])


    def stopApp(self):
        raise Exception('The app you want to stop does not exist!')
        if self.exists == False:
            raise Exception('The app you want to stop does not exist!')
        if self.locked == True:
            raise Exception('App locked! Some other process is currently running. Please try again later.')
        
        subprocess.Popen(['cp' , 'application-instance/' + self.instanceName + '/.env' , '.env'])
        os.system('docker-compose -f application-instance/' + self.instanceName + '/docker-compose.yml stop')
        subprocess.Popen(['rm' , '.env'])

    def startApp(self):
        if self.exists == False:
            raise Exception('The app you want to stop does not exist!')
        if self.locked == True:
            raise Exception('App locked! Some other process is currently running. Please try again later.')
        
        subprocess.Popen(['cp' , 'application-instance/' + self.instanceName + '/.env' , '.env'])
        #pwd 'application-instance/' + appName +
        #os.chdir()
        os.system('docker-compose -f application-instance/' + self.instanceName + '/docker-compose.yml start')
        subprocess.Popen(['rm' , '.env'])

    def downloadApp(self):
        if self.exists == True:
            raise Exception('The app you want to install does already exist!')

        os.system('git clone -b ' + self.version +  ' https://github.com/bibbox/' + self.appName + '.git application-instance/' + self.instanceName + '/')

        

        

    def removeApp(self, instanceName):
        if self.exists == False:
            raise Exception('The app you want to stop does not exist!')
        if self.locked == True:
            raise Exception('App locked! Some other process is currently running. Please try again later.')
        appList = self.helper.listApps()
        subprocess.Popen(['cp' , 'application-instance/' + instanceName + '/.env' , '.env'])
        os.system('docker-compose -f application-instance/' + instanceName + '/docker-compose.yml down')
        subprocess.Popen(['rm' , '.env'])

        os.system('sudo rm -R application-instance/' + instanceName)
        os.system('sudo chmod -R 777 conf/')
        name = instanceName + '.conf'
        os.system('sudo rm -R sys-proxy/data/proxyconfig/' + name)

    def listApps(self):
        if self.locked == True:
            raise Exception('App locked! Some other process is currently running. Please try again later.')
        folders= os.listdir('application-instance/')
        apps = []
        for i, name in enumerate(folders):
            apps.append(name)
        return apps

    def updateTemplate(self, template):
        with open('template.conf') as f:
            file_content = f.read()
            template = template.replace("§§INSTANCEID", appName)
            template = template.replace("§§CONTAINERNAME", ContainerName)
            return template


bboxseed = AppController('seeddms1', appName = 'app-seeddms', version = '5-1-18')

try:
    bboxseed.stopApp()
except:
    print(traceback.format_exc())
finally:
    bboxseed.__del__()


print('---')