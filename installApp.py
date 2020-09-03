#!/usr/bin/env python3

import os
import configparser
import re
import sys
import yaml
import json

# Load available apps
with open('applications.json') as f:
  data = json.load(f)


apps=[]
gitNames=[]
for i in data:
    apps.append(i['name'])
    gitNames.append(i['github_name'])


print('The available apps are: ')
for i, name in enumerate(apps):
  num = str(i)
  print(num + ': ' + name)

index = input('Which app do you want to install? ')
index = int(index)

appName = input("App ID: ")
name = appName + '.conf'

# Check if there are any existing apps
try:
    instApps = os.listdir('apps/')
except:
    instApps = ''


# Clone Repository
os.system('sudo git clone https://github.com/bibbox/' + gitNames[index] + '.git apps/' + appName + '/' + gitNames[index] + '/')

# Check if choosen app name already exists
for instappName in instApps:
    if instappName == appName:
        raise Exception('An app with the same app name is already installed. Please choose another name!')

os.system('cp apps/' + appName + '/' + gitNames[index] + '/.env .env' )

with open('.env') as f:
       file_content = f.read()

words = file_content.split("\n")

string = ''

# Change environment file .env with user settings
print('Please set user parameters!')
for param in words[:-1]:
    param = param.split('=')
    param = param[0]
    if param == 'INSTANCE':
        setvar = appName
        string = string + param + '=' + setvar + '\n'
    elif param == 'PORT':
        setvar = ''
        string = string + param + '=' + setvar + '\n'
    else:
        setvar = input(param + ': ')
        string = string + param + '=' + setvar + '\n'

os.system('sudo chmod -R 777 apps/')

cf = open( '.env', 'w+')
cf.write(string)
cf.close()

ef = open( 'apps/' + appName + '/' + gitNames[index] + '/.env', 'w+')
ef.write(string)
ef.close()


composetemp = 'docker-compose.yml'
path = ('apps/' + appName + '/' + gitNames[index] + '/')


def readContainername(composefile):
    data = yaml.load(composefile)
    for k, v in data["services"].items():
        if 'container_name' in v:
            ContainerName = v.get('container_name')
            ContainerName = ContainerName.replace('${INSTANCE}', appName)
            try:
                ContainerName = ContainerName.replace('-db', '')
            except:
                pass

    return ContainerName

def updateTemplate(template):
    with open('template.conf') as f:
       file_content = f.read()
       template = template.replace("§§INSTANCEID", appName)
       template = template.replace("§§CONTAINERNAME", ContainerName)
    return template


# open compose file
# change instance names to user instance name
stream = open('apps/' + appName + '/' + gitNames[index] + '/docker-compose.yml', 'r')
data = yaml.load(stream)

var1 = data['services']

newkeys = []
oldkeys = []

for key, value in var1.items():
    newkey = key.replace('bibbox', appName)
    newkeys.append(newkey)
    oldkeys.append(key)


for i, key in enumerate(newkeys):
    var1[key] = var1.pop(oldkeys[i])

data['services'] = var1

with open('apps/' + appName + '/' + gitNames[index] + '/docker-compose.yml', 'w+') as yaml_file:
    yaml.dump(data, yaml_file, default_flow_style=False)




composefile = open(path + composetemp, 'r').read()


ContainerName = readContainername(composefile)

template = open('template.conf', 'r').read()
template = updateTemplate(template)


# write to compose file and save
cf = open( path + 'docker-compose-template.yml', 'w+')
cf.write(composefile)
cf.close()

os.system('sudo chmod -R 777 conf/')
target = open( 'conf/sites/' + name, 'w+')
target.write(template)
target.close()


# execute docker compose
os.system('docker-compose -f apps/' + appName + '/' + gitNames[index] + '/docker-compose.yml up -d ')

os.system('docker exec -it local_nginx service nginx reload')
os.system('rm .env')
print('done')
