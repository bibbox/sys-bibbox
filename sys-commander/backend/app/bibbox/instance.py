import os
import json
import inspect


class InstanceDescription  ():
    def __init__(self):
        self.instancename = 'sample-instance'
        self.appname      = 'app-appid'
        self.version      = 'version string'
        self.state        = 'JUSTBORN'

    @classmethod
    def fromdict(cls, descrdict):
        item = cls()
        for key in descrdict: 
            setattr(item, key, descrdict[key]) 
        return item

    @classmethod
    def states (cls):
        # the 'DELETED' state never will be set ....
        return ('JUSTBORN', 'INSTALLING', 'STARTING', 'RUNING', 'STOPPING', 'STOPPED', 'DELETING', 'ERROR', 'DELETED')

class Instance  ():

    """ Class for a BIBBOX INSTANCE - REPRESENTS A DIRECTORY in /opt/bibbox/instances/ """
    BASEURL = '/opt/bibbox/instances/'

    example_description = InstanceDescription.fromdict ({'instancename': 'test', 
                                                         'appname': 'app-seedms', 
                                                         'version': 'development', 
                                                         'state':   'INSTALLING'})

    example_description_as_dict = example_description.__dict__


    def __init__(self, id):
        # test if the directoy exists otherwise raise an exeption and write the appropiate stuff in the log file
        # test if the default config file exists, otherwise log a warning
        # please note that the instance itself is genrated / deleted by the instance_controller and not by the instance class
        self.id = id
  
    @classmethod
    def ids (cls):
        r = os.listdir(cls.BASEURL)
        return r

    def configfile (self, name):
        idescr = self.__readJsonFile (name)
        return idescr

    def instance (self):
        idescr = self.__readJsonFile (inspect.stack()[0][3]  + '.json')
        return idescr

    def appinfo (self):
        idescr = self.__readJsonFile (inspect.stack()[0][3]  + '.json')
        return idescr

    def portinfo (self):
        idescr = self.__readJsonFile (inspect.stack()[0][3]  + '.json')
        return idescr

    def __readJsonFile (self, name):
        path = self.BASEURL + self.id + '/' + name
        reader = open(path, 'r')
        try:
            c = reader.read()
            idescr = json.loads(c)
        finally:
            reader.close()
        return idescr


# some test code for development
# this should finaly be done in an unittest

if __name__ == '__main__':
    print ("====================== INSTANCE CONTROLOER DEVELOPMENT TEST =====================")
    print ("Default Value in the InstanceDescription Class =>", InstanceDescription().__dict__)
    print ("Example Value in the Instance Class            =>", Instance.example_description_as_dict)
    print ("States =>", InstanceDescription.states())

    iIds = Instance.ids ()
  
    print (iIds)
    for id in iIds:
        instance = Instance (id)
        iDescr = instance.instance ()
        print (iDescr)
    print ("======================              DONE                     ====================")
