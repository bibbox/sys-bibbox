import os 
import yaml
import copy

from backend.app.bibbox.file_handler import FileHandler


# TODO can we just initaite the class with the instance name and then read and write the stuff directly from the directory
#      we could also renamoe the class to InstanceHandler, as we are doing template and proxies
#      I would even do the update of the INSTANCE file with the proxy information and other things in this class

class InstanceHandler ():

    
    def __init__(self, template_str, instanceDescr):
        self.template_str = template_str
        self.instanceDescr = instanceDescr

    
    def getCompose (self):

        compose_str = self.__replacePlaceholders(self.instanceDescr)

        keys_to_remove = [
             "proxy", 
             "ports"
            ]

        compose_str = self.__removeKeysFromNestedDict(yaml.safe_load(compose_str), keys_to_remove)
        return compose_str

    def getComposeLocal (self):

        compose_local_str = self.__replacePlaceholders(self.instanceDescr)
        
        keys_to_remove = [
             "proxy", 
             "networks"
            ]

        compose_local_str = self.__removeKeysFromNestedDict(yaml.safe_load(compose_local_str), keys_to_remove)
        
        return compose_local_str
    
    def getProxyInformation (self):

        compose_str = self.__replacePlaceholders(self.instanceDescr)
        proxy_info = []
        services_dict = yaml.safe_load(compose_str)['services']
        for service_key in services_dict.keys():
            if 'proxy' in services_dict[service_key]:

                proxy_entry = {
                    'CONTAINER'     : '',
                    'URLPREFIX'     : '',
                    'TYPE'          : '',
                    'TEMPLATE'      : '',
                    'DISPLAYNAME'   : ''
                }
                # possible bugfix is to asuure type superscriptions yields desired Output
                # e.g.:assert isinstance(services_dict[service_key]['ports'], list) 
                port_suffix = services_dict[service_key]['ports'][0].split(":")[-1]
                proxy_entry['CONTAINER'] = "{}:{}".format(services_dict[service_key]['container_name'], port_suffix)
                for key, value in services_dict[service_key]['proxy'].items():
                    proxy_entry[key] = str(value)

                proxy_info.append(proxy_entry)
        return proxy_info

    def generateProxyFile (self):
        fh = FileHandler()
        config = fh.getBIBBOXconfig ()
        proxy_infomation = self.getProxyInformation ()

        proxyfile_content = ""

        for pi in proxy_infomation:
            if (pi['TEMPLATE'] == 'default'):
                defaultTemplate = fh.getConfigFile ('proxy-default.template')
                proxy = defaultTemplate.replace('§§BASEURL', config['baseurl'])
                proxy = proxy.replace('§§INSTANCEID', pi['URLPREFIX'])
                proxy = proxy.replace('§§CONTAINERNAME', pi['CONTAINER'])
                
                proxyfile_content += proxy + '\n\n'

            elif (pi['TEMPLATE'] == 'websocket'):
                wsTemplate = fh.getConfigFile('proxy-websocket.template')
                proxy = wsTemplate.replace('§§BASEURL', config['baseurl'])
                proxy = proxy.replace('§§INSTANCEID', pi['URLPREFIX'])
                proxy = proxy.replace('§§CONTAINERNAME', pi['CONTAINER'])
                proxy = proxy.replace('§§PATH_TO_SOCKET', pi['PATH_TO_SOCKET'])

                proxyfile_content += proxy + '\n\n'
            
            else:
                defaultTemplate = fh.getConfigFile ('proxy-{}.template'.format(pi['TEMPLATE']))
                proxy = defaultTemplate.replace('§§BASEURL', config['baseurl'])
                proxy = proxy.replace('§§INSTANCEID', pi['URLPREFIX'])
                proxy = proxy.replace('§§CONTAINERNAME', pi['CONTAINER'])

                proxyfile_content += proxy + '\n\n'

        filename = '005-' + self.instanceDescr['instancename'] + '.conf'
        fh.writeProxyFile (filename, proxyfile_content)



    def getContainerNames (self):
        compose_str = self.__replacePlaceholders(self.instanceDescr)
        container_names = []
        
        services_dict = yaml.safe_load(compose_str)['services']

        for key in services_dict.keys():
            if 'container_name' in services_dict[key]:
                container_names.append(services_dict[key]['container_name'])
            
            ## if container_name not explicitly specified, use the service name instead
            ## alternative: enforce container_name to be specified in docker-compose.yml file of new bibbox v4 apps
            # else:
            #     container_names.append(key)

        return container_names


    def __removeKeysFromNestedDict (self, compose_dict, keys_to_remove):
        dict_temp = compose_dict.copy()

        for key in dict_temp.keys():
            if isinstance(dict_temp[key], dict):
                self.__removeKeysFromNestedDict(compose_dict[key], keys_to_remove)

            if key in keys_to_remove:
                try:
                    del compose_dict[key]
                except KeyError as exc:
                    print(exc)

        return compose_dict

    def __replacePlaceholders (self, compose_dict):
        comp_str = self.template_str
        comp_str = comp_str.replace('§§INSTANCE', compose_dict['instancename'])
        # Replace BASEURL with bibbox baseurl
        fh = FileHandler()
        config = fh.getBIBBOXconfig ()
        comp_str = comp_str.replace('§§BASEURL', config['baseurl'])

        # only applicable if §§KEY in docker-compose.yml.template == KEY in instanceDescr['instanceDescr'] (without §§ Prefix)
        # for key, value in self.instanceDescr.items():
        #     if not isinstance(value, dict):
        #         str = str.replace('§§' + key, value)

        for key, value in self.instanceDescr['parameters'].items():
            comp_str = comp_str.replace('§§' + key, value)
        
        return comp_str

### dev testing 
if __name__ == "__main__":  

    dir_path = os.path.dirname(os.path.realpath(__file__))

    print(dir_path)
    with open(dir_path + "/test_output/docker-compose-template-testing.yml", 'r') as template_obj:
        template_str = template_obj.read()

    instanceDescr = {
        "instancename"  : "wptest",
        "displayname"   : "Wordpress Test",
        "app" : {
            "organization": "bibbox",
            "name"        : "app-wordpress",
            "version"     : "V4",
        },
        "parameters"       : 
                {
            "MYSQL_ROOT_PASSWORD" : "quaksi"
        }            
    }

    compose_class_instance = InstanceHandler(template_str, instanceDescr)
    compose_class_instance.generateProxyFile ()

    repeat = 25

    print ("=========================== YAML PARSING DEVELOPMENT TEST =========================")
    print("\n{} {} {}\n".format("-"*repeat, "COMPOSE TEMPLATE ", "-"*repeat))
    print(yaml.dump(yaml.safe_load(compose_class_instance.template_str), default_flow_style=False))

    print("\n{} {} {}\n".format("-"*repeat, "COMPOSE", "-"*repeat))
    print(yaml.dump(compose_class_instance.getCompose(), default_flow_style=False))

    print("\n{} {} {}\n".format("-"*repeat, "COMPOSE LOCAL", "-"*repeat))
    print(yaml.dump(compose_class_instance.getComposeLocal(), default_flow_style=False))

    print("\n{} {} {}\n".format("-"*repeat, "PROXY INFO", "-"*repeat))
    proxy_infos = compose_class_instance.getProxyInformation()
    for _ in proxy_infos:
        print(_)


    print("\n{} {} {}".format("-"*repeat, "CONTAINER NAMES", "-"*repeat))
    print(compose_class_instance.getContainerNames())
    print ("======================              DONE                     ====================")

### testing ende
