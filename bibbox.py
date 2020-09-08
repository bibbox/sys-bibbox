#!/usr/bin/env python3

import os
import json
import yaml
import subprocess



class Bibbox:

    def __init__(self):
        self.helper = Helpers()


    def stopApp(self,appName, instanceName):
        check = self.helper.appExists(appName)
        if check == False:
            raise Exception('The app you want to stop does not exist!')
        appList = self.helper.listApps()
        subprocess.Popen(['cp' , 'application-instance/' + appName + '/.env' , '.env'])
        os.system('docker-compose -f application-instance/' + appName + '/docker-compose.yml stop')
        subprocess.Popen(['rm' , '.env'])

    def startApp(self, appName):
        check = self.helper.appExists(appName)
        if check == False:
            raise Exception('The app you want to start does not exist!')
        appList = self.helper.listApps()
        subprocess.Popen(['cp' , 'application-instance/' + appName + '/.env' , '.env'])
        #pwd 'application-instance/' + appName +
        #os.chdir()
        os.system('docker-compose -f application-instance/' + appName + '/docker-compose.yml start')
        subprocess.Popen(['rm' , '.env'])

    def installApp(appName, version):
        check = self.helper.appExists(appName)
        if check == True:
            raise Exception('The app you want to install does already exist!')
        
        parts = appName.split('-')
        name = parts[1] +'-' + parts[2]

        os.system('sudo git clone https://github.com/bibbox/' + name + '.git application-instance/' + appNameame + '/')
        os.system('cp apps/' + appName + '/' + gitNames[index] + '/.env .env' )

        

    def removeApp(self, appName):
        check = self.helper.appExists(appName)
        if check == False:
            raise Exception('The app you want to start does not exist!')
        appList = self.helper.listApps()
        subprocess.Popen(['cp' , 'application-instance/' + appName + '/.env' , '.env'])
        os.system('docker-compose -f application-instance/' + appName + '/docker-compose.yml down')
        subprocess.Popen(['rm' , '.env'])

        os.system('sudo rm -R application-instance/' + appName)
        os.system('sudo chmod -R 777 conf/')
        name = appName + '.conf'
        os.system('sudo rm -R sys-proxy/data/proxyconfig/' + name)



class Helpers:
    def listApps(self):
        folders= os.listdir('application-instance/')
        apps = []
        for i, name in enumerate(folders):
            #parts = name.split('-')
            #appName = parts[-1]
            apps.append(name)
        return apps

    def appExists(self, appName):
        folders= os.listdir('application-instance/')
        if appName in folders:
            return True
        else: 
            return False

    def updateTemplate(self, template):
        with open('template.conf') as f:
        file_content = f.read()
        template = template.replace("§§INSTANCEID", appName)
        template = template.replace("§§CONTAINERNAME", ContainerName)
        return template


bbox = Bibbox()

bbox.startApp('app-seeddms-seeddms')