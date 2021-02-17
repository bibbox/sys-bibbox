import uuid
import requests
if __name__ == "__main__":
    print ("====================== INSTANCE CONTROLOER DEVELOPMENT TEST =====================")

    res = requests.get('http://127.0.0.1:5010/api/v1/instances')
    print ('response from server:',res.text)

    print("try to call")
    paylod = {
        "appname"     : "app-wordpress",
        "version"     : "V4",
        "displayname" : "Wordpress Test",
        "dataroot"    : "/opt/bibbox/instance-data/",
        "parameters"  : 
            {
                "MYSQL_ROOT_PASSWORD" : "quaksi"
            }            
    }
    res = requests.post('http://127.0.0.1:5010/api/v1/instances/' + str(uuid.uuid4()), json=paylod)
    print ('response from server:',res.text)
    print ("======================              DONE                     ====================")