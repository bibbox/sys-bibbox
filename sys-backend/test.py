import mainFunctions
import helperFunctions

x = mainFunctions.MainFunctions()
h = helperFunctions.AppController()
paramList, instanceName, appName, version = h.getParams('seeddms77777','SeedDMS','master')
paramList = x.setParams(paramList)
newName = 'seeddms2'


x.installApp(paramList,[], instanceName, appName, version)
#x.stopApp(instanceName) 
#status = x.getStatus(instanceName)
#x.startApp(instanceName)
#status1 = x.getStatus(instanceName)
#x.copyApp(instanceName, newName)
#x.removeApp(instanceName)
#appsList = x.listApps()
#installedAppsList = x.listInstalledApps()
#print(appsList, installedAppsList)
#x.startBibbox()
#x.stopBibbox()
#name = x.getAppName('SeedDMS')
pass
