import os
import yaml



stream = open('apps/4/app-seeddmsTNG/docker-compose.yml', 'r')
data = yaml.load(stream)

var1 = data['services']

#dep = var1['depends_on']

newkeys = []
oldkeys = []

for key, value in var1.items():
    try:
        dep = var1[key]['depends_on']
        newdep = key.replace('bibbox', '4')
        var1[key]['depends_on'] = newdep
    except:
        pass    
    newkey = key.replace('bibbox', '4')
    newkeys.append(newkey)
    oldkeys.append(key)


for i, key in enumerate(newkeys):
    var1[key] = var1.pop(oldkeys[i])

data['services'] = var1

with open('apps/4/app-seeddmsTNG/docker-compose.yml', 'w+') as yaml_file:
    yaml.dump(data, yaml_file, default_flow_style=False)

print('done')
