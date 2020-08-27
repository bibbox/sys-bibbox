#!/usr/bin/env python3

import os
import configparser
import re
import sys
import yaml
import json

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

os.system('sudo git clone https://github.com/bibbox/' + gitNames[index] + '.git apps/' + appName + '/' + gitNames[index] + '/')




with open('conf/usersettings/userinputlocal.json', 'w+') as outfile:
    json.dump(data, outfile)


composetemp = 'docker-compose-template.yml'
path = ('apps/' + appName + '/' + gitNames[index] + '/')


def updateCompose(composefile):
    with open(path + composetemp) as f:
       file_content = f.read()
       composefile = composefile.replace("§§INSTANCE", appName)
    return composefile

def readContainername(composefile):
    data = yaml.load(composefile)
    for k, v in data["services"].items():
        if 'container_name' in v:
            ContainerName = v.get('container_name')
    return ContainerName

def updateTemplate(template):
    with open('template.conf') as f:
       file_content = f.read()
       template = template.replace("§§INSTANCEID", appName)
       template = template.replace("§§CONTAINERNAME", ContainerName)
    return template

def testConfigMising(template):
    if(template.find("§§") != -1):
        print("ERROR: there are unchanged Variables in the compose file!!")
        m = re.search('(§§.+)[ :]?', template)
        if m:
            print("Found :" + m.group(1))
        sys.exit(os.EX_DATAERR)



composefile = open(path + composetemp, 'r').read()
composefile = updateCompose(composefile)


ContainerName = readContainername(composefile)

template = open('template.conf', 'r').read()
template = updateTemplate(template)
testConfigMising(template)

os.system('sudo chmod -R 777 apps/')

cf = open( path + 'docker-compose-template.yml', 'w+')
cf.write(composefile)
cf.close()

os.system('sudo chmod -R 777 conf/')
target = open( 'conf/sites/' + name, 'w+')
target.write(template)
target.close()


os.system('docker-compose -f apps/' + appName + '/' + gitNames[index] + '/docker-compose-template.yml up -d')

print('done')
