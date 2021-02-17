#
# docker-compose from template
#
import yaml
import re


class ComposeTemplate ():

    def __init__(self, template, parameters):
    
    def getCompose (self):    
        # gets a valid yaml file, which will be our final docker-compose
        # replace parameters

        # delete proxy and ports entry

    def getComposeLocal (self):    
        # gets a valid yaml file, which will be our final docker-compose
        # replace §§INSTANCE  by 'bibbox
        # delete proxy  entry
        # remove all network entries

    def getProxyInformation (self):    
         # gets the proxy information

        # replace parameters

        # get information for 

        # §§INSTANCE = 'test"
        result = [
            {
            'urlprefix' : 'test',  
            'type' : 'PRIMARY', 
            'container' : 'test-wordpress:80',
            'template'  : 'default',
            'displayname' : 'Wordpress'
            },
            {
            'urlprefix' : 'test-adminer',  
            'type' : 'HELPER', 
            'container' : 'test-wordpress-adminer:8080',
            'template'  : 'default',
            'displayname' : 'Adminer'
            }
        ]
            
    def getContainerNames (self):    




def generateComposeFromTemplate(
        instancename: str, 
        db_password: str, 
        dataroot: str,
        filepath_to_template: str,
        filepath_to_output: str) -> str:

    status = 'ok'
    parameter_values_dict = {
        "§§INSTANCE"            : instancename, 
        "§§MYSQL_ROOT_PASSWORD" : db_password, 
        "§§DATAROOT"            : dataroot
        }

    temporary_file = None

    with open(filepath_to_template + "docker-compose-template.yml", 'r') as template:
        try:
            temporary_file = re.sub(r'§§[A-Z_]+', lambda match: parameter_values_dict.get(match.group()), template.read())
        except yaml.YAMLError as exception:
            status = "error occurred"
            print(exception)

    with open(filepath_to_output + "docker-compose.yml", 'w+') as out:
        try:
            yaml.dump(yaml.safe_load(temporary_file), out, default_flow_style=False)
        except yaml.YAMLError as exception:
            status = "error occurred"
            print(exception)

    return status