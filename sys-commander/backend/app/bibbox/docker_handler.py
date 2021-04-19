import docker
import os
import subprocess

class DockerHandler():

    def __init__(self):
        self.client = docker.from_env()
        self.INSTANCEPATH = "/opt/bibbox/instances/"


    def docker_stopInstance(self, instance_name):
        try:
            # TODO:
            # shell=True is a security hazard, so we must sanitize the input
            command = f"cd {self.INSTANCEPATH}{instance_name}; docker-compose stop"
            subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8", shell=True)
            
        except Exception as ex:
            print(ex)

    def docker_startInstance(self, instance_name):
        try:
            # TODO:
            # shell=True is a security hazard, so we must sanitize the input
            command = f"cd {self.INSTANCEPATH}{instance_name}; docker-compose start"
            subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8", shell=True)
            
        except Exception as ex:
            print(ex)

    

    def docker_getContainerLogs(self, instance_name):
        container_logs_dict = {}
        containers = self.client.containers.list(filters={"label":["com.docker.compose.project={}".format(instance_name)]})
        
        for container in containers:
            container_logs_dict[container.name] = str(container.logs(tail=200))[3:-1].split('\\n')

            ## subprocess implementation
            # command = 'docker logs {} --tail 200'.format(container.name).split()
            # process = subprocess.run(command, capture_output=True)
            # logs_from_container = process.stderr

            # container_logs_dict[container.name] = logs_from_container.split('\n')
        
        return container_logs_dict

    def docker_deleteStoppedContainers(self, instance_name):
        removed = self.client.containers.prune(filters={"label":["com.docker.compose.project={}".format(instance_name)]})
        status = ""
        if removed['ContainersDeleted']:
            status = "Removed containers: {}".format([x for x in removed['ContainersDeleted']])
            print(status)
        else:
            status = "No containers to remove."
            print(status)
    

    def __stopContainers(self, containers):
        for container in containers:
            print("Stopping container: {}...  ".format(container.name), end="")
            container.stop()
            print("Stopped container: {}.\n".format(container.name))    

    
