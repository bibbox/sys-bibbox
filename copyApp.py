#!/usr/bin/env python3

import os

print('Wich app do you want to copy? ')
appName = input('Please enter app name: ')

print('Please enter the name of the new app! ')
newappName = input('Please enter new app name: ')

instApps = os.listdir('apps/')

if appName in instApps:
    pass
else:
    raise Exception('Your coosen app with the name ' + appName + ' does not exist!')

os.system('sudo chmod -R 777 apps')

folder= os.listdir('apps/'+ appName )
gitName = folder[0]
datadir = 'apps/' + appName + '/' + gitName + '/data'

os.system('sudo git clone https://github.com/bibbox/' + gitName + '.git apps/' + newappName + '/' + gitName + '/')
os.system('sudo rm -R apps/' + newappName + '/' + gitName + '/data')
os.system('sudo cp -R ' + datadir + ' apps/' + newappName + '/' + gitName + '/data')

print('done')