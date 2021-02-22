
import requests 
import json 
import os

from backend.app.bibbox.instance import InstanceDescription

# add gitpython to requirements.txt

# TODO
#
# to overcome the 'RAW CACHE' problem, we have to use git directly
# this seems to be the standard lib
# https://gitpython.readthedocs.io/en/stable/tutorial.html
#
# then it would make sense to mit the Github functions in a seperate class
# which makes a local copy/cache of the github repository with the correct 
# version. 
# 
# in offline mode, we couöd then just read from the local dir
#  => we need a global config saying, that we work in offline mode 
#  => and a cache-all function downling all the reproes and builiding all images
#  


class FileManager():
    
    def __init__(self):
        self.INSTANCEPATH = "/opt/bibbox/instances/"
        self.CONFIGPATH   = "/opt/bibbox/config/"
        self.PROXYPATH    = "/opt/bibbox/proxy/"

    def copyFileFromWeb (self, fileurl, instancename, filename):
        try:
            download = requests.get(fileurl).content
        except Exception:
            raise Exception('Something went wrong during connecting to the Web. Please Check your internet connection!')

        filename =  self.INSTANCEPATH  + instancename + "/" + filename

        with open(filename, 'wb') as f:
            f.write(download)
    
    def copyFileFromGithub (self, organization, repository, version, filename, instancename, destinationfilename):
        #
        # TODO replace this with the local 'roberts' variant
        #      (after a first protype of the frontend is running) 
        #
        fileurl = self.__getBaseUrlRaw (organization, repository, version) + '/' + filename
        self.copyFileFromWeb (fileurl, instancename, destinationfilename)

    def copyAllFilesToInstanceDirectory (self, instanceDescr):

        instancename = instanceDescr['instancename']
        organization = instanceDescr['app']['organization']
        repository = instanceDescr['app']['name']
        version    = instanceDescr['app']['version']

        for fn in ('docker-compose-template.yml', 'fileinfo.json', 'appinfo.json'):
            self.copyFileFromGithub (organization, repository, version, fn , instancename,  fn)

        filename =  self.INSTANCEPATH  + instancename + "/" + 'fileinfo.json'
        with open(filename, 'r') as f:
            fileinfo = json.load (f)

        for directory_to_copy in fileinfo['makefolders']: 
            dirname =  self.INSTANCEPATH  + instancename + "/" + directory_to_copy
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            
        for file_to_copy in fileinfo['copyfiles']:
            source = file_to_copy["source"]
            destination = file_to_copy["destination"]
            if ('https://' in source or 'http://' in source):
                self.copyFileFromWeb    (source, instancename,  destination)
            else:
                self.copyFileFromGithub (organization, repository, version, source, instancename,  destination)

    def getConfigFile (self, name):
         filename =  self.CONFIGPATH  + name
         with open(filename, 'r') as f:
            content = f.read ()
         return content 

    # should we make for the config a own class, or even integrae it into the FLASK confid ?
    def getBIBBOXconfig (self):
        path =  self.CONFIGPATH  + 'bibbox.config'
        config   = self.__readJsonFile (path)
        return config
        
    def writeProxyFile (self, name, content):
         filename =  self.PROXYPATH + 'sites/' + name
         with open(filename, 'w') as f:
            f.write (content)
         return content 

    def __getBaseUrlRaw (self, organization, repository, version):
        burl = ''
        if version == 'development':
            burl = 'https://raw.githubusercontent.com/' + organization + '/' + repository   + '/master/'
        else:
            burl = 'https://raw.githubusercontent.com/'  + organization + '/' + repository   + '/' + version + '/'
        return burl

    def __readJsonFile (self, path):
        reader = open(path, 'r')
        try:
            c = reader.read()
            idescr = json.loads(c)
        finally:
            reader.close()
        return idescr


    # does this function belong in this class? wip
    # good question 
        
    def updateInstanceState(self, path_to_file, state_to_set):
        if state_to_set in InstanceDescription().states():
            with open(path, 'w') as f: 
                instanceDescr['state'] = state_to_set
                simplejson.dump (instanceDescr, f)
        else:
            raise Exception("Trying to set unknown App State")
                

