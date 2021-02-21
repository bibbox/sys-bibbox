import uuid
import requests
if __name__ == "__main__":


    print ("====================== INSTANCE CONTROLOER DEVELOPMENT TEST =====================")

    res = requests.get('http://127.0.0.1:5010/api/v1/instances')
    print ('response from server:',res.text)

    res = requests.get('http://127.0.0.1:5010/api/v1/instances/pong')
    print ('response from server:',res.text)
    print ("======================              DONE                     ====================") 

    instanceName = str(uuid.uuid4())
    instanceName = 'wptest02'

    print("try to make the instance", instanceName)
    payload = {
        "displayname" : "Wordpress Test",
        "app" : {
            "organization": "bibbox",
            "name"        : "app-wordpress",
            "version"     : "V4",
        },
        "parameters"  : 
            {
                "MYSQL_ROOT_PASSWORD" : "quaksi"
            }            
    }
    res = requests.post('http://127.0.0.1:5010/api/v1/instances/' + instanceName, json=payload)
    print ('response from server:',res.text)


    