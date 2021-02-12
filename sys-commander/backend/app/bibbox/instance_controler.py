import os
import json


 
class InstanceControler ():

  """Controler Class for the BIBBOX INSTANCES """

  def __init__(self, baseUrl ='/opt/bibbox/instances/'):
      # text if the directoy exists otherwise raise an exeption and write the appropiate stuff in the log file
      self.baseUrl = baseUrl

#
# how should we name the functions, with get or without get 

  def getInstanceIds (self):
      # we need some error handling here
      list = os.listdir(self.baseUrl)
      return list

  def getInstanceDescription (self, id):
      path = self.baseUrl + id + "/instance.json"
      with open(path) as f: 
          idescr = json.load(f)
      return idescr

# some test code for development
# this should finaly be made in an unittest

if __name__ == '__main__':
    print ("====================== INSTANCE CONTROLOER DEVELOPMENT TEST =====================")
    ic = InstanceControler()
    iIds = ic.getInstanceIds ()
    print (iIds)
    for id in iIds:
        iDescr = ic.getInstanceDescription (id)
        print (iDescr)
    print ("======================              DONE                     ====================")
