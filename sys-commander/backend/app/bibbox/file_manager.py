import requests 
import json 
import os
# add gitpython to requirements.txt





class FileManager():
    def __init__(self):
        self.DEFAULTPATH = "/opt/bibbox/instances/"


    def copyFileFromWeb   (self, fileurl, instancename, filename):
        try:
            download = requests.get(fileurl).content
            print (fileurl)
            #print (download)
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


if __name__ == "__main__":
    print ("====================== FILENMANAGER DEVELOPMENT TEST =====================")
    fm = FileManager()

    download_files  = ['docker-compose-template.yml', 'fileinfo.json', 'appinfo.json']
    for fn in download_files:
        fm.copyFileFromGithub ('bibbox', 'app-wordpress', 'V4', fn , '4773d31a-20f0-4d21-83a0-9686e9d6cb1e',  fn)


    filename =  fm.DEFAULTPATH  + '4773d31a-20f0-4d21-83a0-9686e9d6cb1e' + "/" + 'fileinfo.json'
    with open(filename, 'r') as f:
        fileinfo = json.load (f)

    for dtc in fileinfo['makefolders']: 
        dirname =  fm.DEFAULTPATH  + '4773d31a-20f0-4d21-83a0-9686e9d6cb1e' + "/" + dtc
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
    for ftc in fileinfo['copyfiles']:
        src = ftc["source"]
        dest = ftc["destination"]
        print (src, dest)
        if ('https://' in src or 'http://' in src):
            fm.copyFileFromWeb    (src, '4773d31a-20f0-4d21-83a0-9686e9d6cb1e',  dest)
        else:
            fm.copyFileFromGithub ('bibbox', 'app-wordpress', 'V4', src, '4773d31a-20f0-4d21-83a0-9686e9d6cb1e',  dest)


    print ("======================              DONE                     ====================")



