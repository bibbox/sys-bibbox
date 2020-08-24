import json

with open('applications.json') as f:
  data = json.load(f)

apps=[]
for name in data:
    apps.append(name['name'])
print(apps)


