import os
import json

print('Wich app do you want to remove? ')
appName = input('Please enter app name: ')

os.system('cd apps/' + appName)
os.system('docker-compose down')
os.system('cd ..')
os.system('cd ..')

os.system('sudo rm -R apps/' + appName)

os.system('sudo chmod -R 777 conf/')

name = appName + '.conf'
os.system('sudo rm -R conf/sites/' + name)




print('done')