import os
import json

print('Wich app do you want to remove? ')
appName = input('Please enter app name: ')

os.system('sudo chmod -R 777 apps')

instApps = os.listdir('apps/'+ appName)

folder = instApps[0]

os.system('docker-compose -f apps/' + appName +'/' +  folder + '/docker-compose-template.yml down ')

os.system('sudo rm -R apps/' + appName)

os.system('sudo chmod -R 777 conf/')

name = appName + '.conf'
os.system('sudo rm -R conf/sites/' + name)


print('done')