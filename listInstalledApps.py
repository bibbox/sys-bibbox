import os
import json

os.system('sudo chmod -R 777 conf/')
with open('conf/usersettings/userinput.json') as json_file:
    data = json.load(json_file)

    apps = data['instance']
    print('Your installed apps are')
    for i in range(len(apps)):
        subdict = apps[i]
        for subkey in subdict:
            subvalue = subdict[subkey]
            print('App name: ' + subvalue)
            print('Docker Container: ' + subkey)
            print('------------------------------')
            