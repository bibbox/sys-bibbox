import json

with open('applications.json') as f:
  data = json.load(f)

apps=[]
for name in data:
    apps.append(name['name'])

for i, name in enumerate(apps):
  num = str(i)
  print(num + ': ' + name)

#print(apps)


