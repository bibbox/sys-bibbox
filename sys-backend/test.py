from os.path import dirname, abspath
import os
#d = dirname(dirname(abspath(__file__)))
#appPath = d + '/application-instance'
#print('---')


os.system('sudo git clone -b ' + '6-0-11' + ' https://github.com/bibbox/' + 'app-seeddms' + '.git application-instance/' + 'test' + '/')
os.system('sudo git clone -b ' + self.version +  ' https://github.com/bibbox/' + self.appName + '.git application-instance/' + self.instanceName + '/ .')
#git clone --single-branch --branch <branchname>