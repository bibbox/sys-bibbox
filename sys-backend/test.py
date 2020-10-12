import bibboxbackend

x = bibboxbackend.MainFunctions()
paramList, instanceName, appName, version = x.getParams('seeddms7777777','SeedDMS','master')
paramList = x.setParams(paramList)
newName = 'seeddms2'


#x.installApp(paramList,[], instanceName, appName, version)
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
name = x.getAppName('SeedDMS')
pass
