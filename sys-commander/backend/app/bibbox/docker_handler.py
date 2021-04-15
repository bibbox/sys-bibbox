import docker
import os
import subprocess

class DockerHandler():

    def __init__(self):
        self.client = docker.from_env()


    # unused
    def docker_stopAllApps(self):
        app_containers = []
        for container in self.client.containers.list():
            if "bibbox-sys-commander" not in container.name:
                app_containers.append(container)

        self.__stopContainers(app_containers)


    # TODO: docker-compose stop
    def docker_stopInstance(self, instance_name):
        instance_containers = []
        for container in self.client.containers.list():
            if "{}-".format(instance_name) in container.name:
                instance_containers.append(container)
            
        self.__stopContainers(instance_containers)  


    # unused
    def docker_deleteAllStoppedApps(self):
        # TODO: exclude bibbox-sys-commander-* containers

        print("Removing stopped containers...")
        removed = self.client.containers.prune()
        if removed['ContainersDeleted']:
            print("Removed containers: {}".format([container_id for container_id in removed['ContainersDeleted']]))
        else:
            print("No containers to remove.")

    def docker_getContainerNames(self, instance_name):
        return {'testname' : 'testlog'}

    def docker_getContainerLogs(self, instance_name):
        container_logs_dict = {}
        containers = self.client.containers.list(filters={"label":["com.docker.compose.project={}".format(instance_name)]})
        
        for container in containers:
            container_logs_dict[container.name] = str(container.logs(tail=200)).split('\\n')

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

    
