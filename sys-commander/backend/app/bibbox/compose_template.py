import yaml


class ComposeTemplate ():

    def __init__(self, template_str, payload):
        self.template_str = template_str
        self.payload = payload

    #### todo: add more validators
    # @property
    # def template_str(self):
    #     return self._template_str

    # @template_str.setter
    # def template_str(self, template_str):
    #     if not len(template_str): raise Exception("Instantiating failed. Empty Template String.")
    #     self._template_str = template_str

    
    def getCompose (self):

        compose_str = self.__replacePlaceholders(self.payload)
        keys_to_remove = [
             "proxy", 
             "ports"
            ]

        compose_str = self.__removeKeysFromNestedDict(yaml.safe_load(compose_str), keys_to_remove)

        return compose_str

    def getComposeLocal (self):

        modified_payload = self.payload
        modified_payload['instancename'] = 'bibbox'

        compose_local_str = self.__replacePlaceholders(modified_payload)

        keys_to_remove = [
             "proxy", 
             "ports", 
             "networks"
            ]

        compose_local_str = self.__removeKeysFromNestedDict(yaml.safe_load(compose_local_str), keys_to_remove)
        
        return compose_local_str
    
    def getProxyInformation (self):

        compose_str = self.__replacePlaceholders(self.payload)
        proxy_info = []
        services_dict = yaml.safe_load(compose_str)['services']



        for key in services_dict.keys():
            if 'proxy' in services_dict[key]:
                proxy_entry = {
                    'urlprefix'     : '',
                    'type'          : '',
                    'template'      : '',
                    'displayname'   : '',
                    'container'     : ''
                }
                port_suffix = services_dict[key]['ports'][0].split(":")[-1]
                proxy_entry['container'] = "{}:{}".format(services_dict[key]['container_name'], port_suffix)
                for kv_pair in services_dict[key]['proxy']:
                    for key in kv_pair:
                        proxy_entry[key] = kv_pair.get(key)
                proxy_info.append(proxy_entry)

        return proxy_info
            
    def getContainerNames (self):
        compose_str = self.__replacePlaceholders(self.payload)
        container_names = []
        
        services_dict = yaml.safe_load(compose_str)['services']

        for key in services_dict.keys():
            if 'container_name' in services_dict[key]:
                container_names.append(services_dict[key]['container_name'])

        return container_names

    def __removeKeysFromNestedDict(self, compose_dict, keys_to_remove):
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

    def __replacePlaceholders(self, compose_dict):
        str = self.template_str
        str = str.replace('§§INSTANCE', compose_dict['instancename'])
        str = str.replace('§§DATAROOT', compose_dict['dataroot'][:-1]) # [:-1] to remove trailing /
        
        # only applicable if §§KEY in docker-compose-template.yml == KEY in payload['payload'] (without §§ Prefix) 
        # for key, value in self.payload.items():
        #     if not isinstance(value, dict):
        #         str = str.replace('§§' + key, value)

        for key, value in self.payload['payload'].items():
            str = str.replace('§§' + key, value)

        return str

### testing 
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)
with open(dir_path + "/test_output/docker-compose-template-testing.yml", 'r') as template_obj:
    template_str = template_obj.read()

    payload = {
        "appname"       : "app-wordpress",
        "instancename"  : "app-wordpress-instance", #id
        "version"       : "V4",
        "displayname"   : "Wordpress Test",
        "dataroot"      : "/opt/bibbox/instance-data/",
        "payload"       : 
                    {
                        "MYSQL_ROOT_PASSWORD" : "quaksi"
                    }            
    }

    compose_class_instance = ComposeTemplate(template_str, payload)
    # compose_class_instance = ComposeTemplate(template_str, ["test-instance-Name", "/opt/test/directory", "test_pw"])

repeat = 50

print("\n{} {} {}\n".format("#"*repeat, "COMPOSE TEMPLATE ", "#"*repeat))
print(yaml.dump(yaml.safe_load(compose_class_instance.template_str), default_flow_style=False))

print("\n{} {} {}\n".format("#"*repeat, "COMPOSE", "#"*repeat))
print(yaml.dump(compose_class_instance.getCompose(), default_flow_style=False))

print("\n{} {} {}\n".format("#"*repeat, "COMPOSE LOCAL", "#"*repeat))
print(yaml.dump(compose_class_instance.getComposeLocal(), default_flow_style=False))

print("\n{} {} {}\n".format("#"*repeat, "PROXY INFO", "#"*repeat))
proxy_infos = compose_class_instance.getProxyInformation()
for _ in proxy_infos:
    print(_)


print("\n{} {} {}\n".format("#"*repeat, "CONTAINER NAMES", "#"*repeat))
print(compose_class_instance.getContainerNames())
print("\n")

### testing ende