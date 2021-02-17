#
# docker-compose from template
#

import yaml
import re

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