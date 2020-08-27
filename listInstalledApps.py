import os
import json

instApps = os.listdir('apps/')

print('Your installed apps are: ')
for appName in instApps:
    print(appName) 

            