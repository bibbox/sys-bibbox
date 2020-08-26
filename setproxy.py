import os
import configparser
import re
import sys
import shutil

userid = input("App ID: ")
containerName = input("Container Name: ")
#path = 'sites/' + userid + '.conf'
name = userid + '.conf'
#os.system('sudo touch ' + path)


def updateCompose(composefile):
    with open('template.conf') as f:
       file_content = f.read()
       #cp = configparser.RawConfigParser()#allow_no_value=True)
       #cp.read_string(file_content) #, encoding='utf-8-sig')
       template = template.replace("§§INSTANCEID", userid)
       template = template.replace("§§CONTAINERNAME", containerName)
    return template

def updateTemplate(template):
    with open('template.conf') as f:
       file_content = f.read()
       #cp = configparser.RawConfigParser()#allow_no_value=True)
       #cp.read_string(file_content) #, encoding='utf-8-sig')
       template = template.replace("§§INSTANCEID", userid)
       template = template.replace("§§CONTAINERNAME", containerName)
    return template

def testConfigMising(template):
    if(template.find("§§") != -1):
        print("ERROR: there are unchanged Variables in the compose file!!")
        m = re.search('(§§.+)[ :]?', template)
        if m:
            print("Found :" + m.group(1))
        sys.exit(os.EX_DATAERR)


template = open('template.conf', 'r').read()

template = updateTemplate(template)

testConfigMising(template)


#target = open("/conf/sites/" + name, 'w+')
target = open( 'conf/sites/' + name, 'w+')

target.write(template)
#shutil.copy2(name, "conf/sites/" + name)
target.close()


print('done')
