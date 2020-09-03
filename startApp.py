#!/usr/bin/env python3

import os

print('Wich app do you want to start? ')
appName = input('Please enter app name: ')

try:
    instApps = os.listdir('apps/')
except:
    instApps = ''

if appName not in instApps:
    raise Exception('The app you want to start does not exist!')

folder= os.listdir('apps/'+ appName )
gitName = folder[0]

os.system('cp apps/' + appName + '/' + gitName + '/.env .env')
output = os.system('docker-compose -f apps/' + appName + '/' + gitName + '/docker-compose.yml start') # --project-directory=apps/' + appName + '/' + gitName)
os.system('rm .env')
print('done')