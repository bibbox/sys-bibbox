
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

    def checkDirectoryStructure(self):
        # checks if the dirs (instances, config, proxy) exist and creates them if not
        try:
            for k, v in vars(self).items():
                if not os.path.exists(v):
                    os.makedirs(v)
            status = 'ok'
        except Exception:
            status = Exception
        return status

    def updateInstanceJSON (self, instance_name, state_to_set):
        # TODO
        # - are we here in the right directory ?    --> now we are
        # - why only update the prxy file ?         --> we wanted to add the proxy infos to the instance.json file. should we do that still?

        # read content from file
        content = self.__readJsonFile(self.INSTANCEPATH + instance_name + "/instance.json")

        # set state of instance
        # info: may soon be deprecated as we modify the instance / instanceDescription class
        if state_to_set not in InstanceDescription().states():
            raise Exception("Error occurred during update of instance.json: Trying to set unknown instance state.")
        else:
            content["state"] = state_to_set

        # add proxy info if not already set
        if "proxy" not in content:
            content["proxy"] = "TODO"
    
        
        # write updated content to instance.json file
        try:     
            with open(self.INSTANCEPATH + instance_name + '/instance.json', 'w+') as f:
                f.truncate(0)
                f.write (json.dumps(content))
        except IOError as ex:
                print(ex + " Error occurred while trying to update instance.json file.")


        # to keep the instances.json file updated
        self.writeInstancesJsonFile()

        # TODO
        # decide if this is the way we want to handle it, or do we first call the writeInstancesJsonFile() function whenever we want to access instances.json

    def writeInstancesJsonFile (self):
        content = {}
        for instance_name in os.listdir(self.INSTANCEPATH):
            if os.path.isdir(self.INSTANCEPATH + instance_name):
                content[instance_name] = self.__readJsonFile(self.INSTANCEPATH + instance_name + '/instance.json')
        with open(self.INSTANCEPATH + 'instances.json', 'w+') as f:
            f.truncate(0)
            f.write (json.dumps(content))

    def getInstancesJSONFile (self):
         filename =  self.INSTANCEPATH  + 'instances.json'
         with open(filename, 'r') as f:
            content = f.read ()
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
