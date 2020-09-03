#!/usr/bin/env python3

import os

print('Wich app do you want to start? ')
appName = input('Please enter app name: ')

folder= os.listdir('apps/'+ appName )
gitName = folder[0]

try:
    instApps = os.listdir('apps/')
except:
    instApps = ''

if appName not in instApps:
    raise Exception('The app you want to start does not exist!')

os.system('cp apps/' + appName + '/' + gitName + '/.env .env')
output = os.system('docker-compose -f apps/' + appName + '/' + gitName + '/docker-compose.yml stop') # --project-directory=apps/' + appName + '/' + gitName)
os.system('rm .env')
print('done')