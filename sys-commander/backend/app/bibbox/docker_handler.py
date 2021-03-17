import docker
import os

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
            print("Removed containers: {}".format([x for x in removed['ContainersDeleted']]))
        else:
            print("No containers to remove.")


    # TODO
    def docker_getContainerLogs(self, container_name):
        pass

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

    
