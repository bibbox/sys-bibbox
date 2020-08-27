import os
import json

print('Wich app do you want to remove? ')
appName = input('Please enter app name: ')

os.system('sudo rm -R apps/' + appName)


name = appName + '.conf'
os.system('sudo rm -R conf/sites/' + name)

os.system('sudo chmod -R 777 conf/')


print('done')