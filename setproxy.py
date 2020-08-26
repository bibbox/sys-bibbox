#!/usr/bin/env python3

import os
import configparser
import re
import sys
import yaml

appName = input("App ID: ")
containerInstance = input("Container Instance: ")
#path = 'sites/' + userid + '.conf'
name = appName + '.conf'
#os.system('sudo touch ' + path)

composetemp = 'docker-compose-template.yml'
path = ('apps/app-seeddmsTNG/')

def updateCompose(composefile):
    with open(path + composetemp) as f:
       file_content = f.read()
       #cp = configparser.RawConfigParser()#allow_no_value=True)
       #cp.read_string(file_content) #, encoding='utf-8-sig')
       composefile = composefile.replace("§§INSTANCE", containerInstance)
    return composefile

def readContainername(composefile):
    data = yaml.load(composefile)
    for k, v in data["services"].items():
        if 'container_name' in v:
        #if data["services"][k].has_key("container_name"):
            #print(data["services"][k]["container_name"]) 
            #ContainerName = data["services"][k]["container_name"]
            ContainerName = v.get('container_name')
    return ContainerName

def updateTemplate(template):
    with open('template.conf') as f:
       file_content = f.read()
       #cp = configparser.RawConfigParser()#allow_no_value=True)
       #cp.read_string(file_content) #, encoding='utf-8-sig')
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

cf = open( path + 'docker-compose.yml', 'w+')
cf.write(composefile)
cf.close()


target = open( 'conf/sites/' + name, 'w+')
target.write(template)
target.close()

print('done')
