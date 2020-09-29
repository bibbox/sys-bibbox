import bibboxbackend

x = bibboxbackend.AppController()
paramList, instanceName, appName, version = x.getParams('test7','app-seeddmsTNG','master')
paramList = x.setParams(paramList)



x.installApp(paramList, instanceName, appName, version)
x.stopApp(instanceName) 
status = x.getStatus(instanceName)
x.startApp(instanceName)
status1 = x.getStatus(instanceName)
x.copyApp('test7', 'testappnew')
#x.removeApp(instanceName)
appsList = x.listApps()
installedAppsList = x.listInstalledApps()
print(appsList, installedAppsList)

