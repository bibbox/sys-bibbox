import requests 
import json 
import os
# add gitpython to requirements.txt



instancename = "a9ba2c6e-f183-4480-a353-bbe13f1b802e"

class FileManager():
    def __init__(self):
        self.DEFAULTPATH = "/opt/bibbox/instances/"


    def copyFileFromWeb (self, fileurl, instancename, filename):
        try:
            download = requests.get(fileurl).content
            print (fileurl)
        except Exception:
            raise Exception('Something went wrong during connecting to the Web. Please Check your internet connection!')

        filename =  self.DEFAULTPATH  + instancename + "/" + filename

        with open(filename, 'wb') as f:
            f.write(download)
    
    def copyFileFromGithub (self, organization, repository, version, filename, instancename, destinationfilename):
        fileurl = self.__getBaseUrlRaw (organization, repository, version) + '/' + filename
        self.copyFileFromWeb (fileurl, instancename, destinationfilename)


    def __getBaseUrlRaw (self, organization, repository, version):
        burl = ''
        if version == 'development':
            burl = 'https://raw.githubusercontent.com/' + organization + '/' + repository   + '/master/'
        else:
            burl = 'https://raw.githubusercontent.com/'  + organization + '/' + repository   + '/' + version + '/'
        return burl


    # does this function belong in this class? wip
    from backend.app.bibbox.instance import InstanceDescription
    
    def updateInstanceState(self, path_to_file, state_to_set):
        if state_to_set in InstanceDescription().states():
            with open(path, 'w') as f: 
                instanceDescr['state'] = state_to_set
                simplejson.dump (instanceDescr, f)
        else:
            raise Exception("Trying to set unknown App State")
                



if __name__ == "__main__":
    print ("====================== FILENMANAGER DEVELOPMENT TEST =====================")
    file_manager = FileManager()

    download_files  = ['docker-compose-template.yml', 'fileinfo.json', 'appinfo.json']
    for fn in download_files:
        file_manager.copyFileFromGithub ('bibbox', 'app-wordpress', 'V4', fn , instancename,  fn)


    filename =  file_manager.DEFAULTPATH  + instancename + "/" + 'fileinfo.json'
    with open(filename, 'r') as f:
        fileinfo = json.load (f)

    for directory_to_copy in fileinfo['makefolders']: 
        dirname =  file_manager.DEFAULTPATH  + instancename + "/" + directory_to_copy
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
    for file_to_copy in fileinfo['copyfiles']:
        source = file_to_copy["source"]
        destination = file_to_copy["destination"]
        print (source, destination)
        if ('https://' in source or 'http://' in source):
            file_manager.copyFileFromWeb    (source, instancename,  destination)
        else:
            file_manager.copyFileFromGithub ('bibbox', 'app-wordpress', 'V4', source, instancename,  destination)


    print ("======================              DONE                     ====================")



