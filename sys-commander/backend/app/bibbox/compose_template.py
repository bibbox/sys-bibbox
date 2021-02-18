import yaml
import re


class ComposeTemplate ():

    def __init__(self, template_str, parameters):
        self.template_str = template_str
        self.parameters = parameters
        self.parameter_dict = {
                "§§INSTANCE"            : self.parameters[0], 
                "§§MYSQL_ROOT_PASSWORD" : self.parameters[1], 
                "§§DATAROOT"            : self.parameters[2]
            }

    #### todo: add more validators
    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        if len(parameters) < 3: raise Exception("Instantiating failed. Too few parameters. Expected 3")
        if len(parameters) > 3: raise Exception("Instantiating failed. Too many parameters. Expected 3")
        self._parameters = parameters

    
    def getCompose (self):

        temp_file_str = self.__replacePlaceholders(self.parameter_dict)

        keys_to_remove = [
             "proxy", 
             "ports"
            ]

        temp_file_str = self.__removeKeysFromNestedDict(yaml.safe_load(temp_file_str), keys_to_remove)

        return temp_file_str

    def getComposeLocal (self):

        modified_parameter_dict = self.parameter_dict.copy()
        modified_parameter_dict['§§INSTANCE'] = 'bibbox'

        temp_file_str = self.__replacePlaceholders(modified_parameter_dict)

        keys_to_remove = [
             "proxy", 
             "ports", 
             "networks"
            ]

        temp_file_str = self.__removeKeysFromNestedDict(yaml.safe_load(temp_file_str), keys_to_remove)
        
        return temp_file_str
    
    def getProxyInformation (self):

        temp_file_str = self.__replacePlaceholders(self.parameter_dict)

        proxy_info = []
        services_dict = yaml.safe_load(temp_file_str)['services']

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

        temp_file_str = self.__replacePlaceholders(self.parameter_dict)
        container_names = []
        services_dict = yaml.safe_load(temp_file_str)['services']

        for key in services_dict.keys():
            if 'container_name' in services_dict[key]:
                container_names.append(services_dict[key]['container_name'])

        return container_names

    def __removeKeysFromNestedDict(self, passed_dict, keys_to_remove):
        dict_temp = passed_dict.copy()

        for key in dict_temp.keys():
            if isinstance(dict_temp[key], dict):
                self.__removeKeysFromNestedDict(passed_dict[key], keys_to_remove)

            if key in keys_to_remove:
                try:
                    del passed_dict[key]
                except KeyError as exc:
                    print(exc)

        return passed_dict

    def __replacePlaceholders(self, passed_dict):
        return re.sub(r'§§[A-Z_]+', lambda match: passed_dict.get(match.group()), self.template_str)

#### testing 
with open("docker-compose-template-testing.yml", 'r') as template_obj:
    template_str = template_obj.read()
    compose_class_instance = ComposeTemplate(template_str, ["test-instance-Name", "test_pw", "/opt/test/directory"])


repeat = 50
print("\n{} {} {}\n".format("#"*repeat, "COMPOSE", "#"*repeat))
print(yaml.dump(compose_class_instance.getCompose(), default_flow_style=False))

print("\n{} {} {}\n".format("#"*repeat, "COMPOSE LOCAL", "#"*repeat))
print(yaml.dump(compose_class_instance.getComposeLocal(), default_flow_style=False))

print("\n{} {} {}\n".format("#"*repeat, "PROXY INFO", "#"*repeat))
proxy_infos = compose_class_instance.getProxyInformation()
print("{}\n{}".format(proxy_infos[0], proxy_infos[1]))

print("\n{} {} {}\n".format("#"*repeat, "CONTAINER NAMES", "#"*repeat))
print(compose_class_instance.getContainerNames())
print("\n")

### testing ende