import docker
import os

class ContainerHelper():

    def __init__(self):
        self.client = docker.from_env()


    def stopAllAppContainers(self):
        app_containers = []
        for container in self.client.containers.list():
            if "bibbox-sys-commander" not in container.name:
                app_containers.append(container)

        self.__stopContainers(app_containers)


    def stopInstanceContainers(self, instance_name):
        instance_containers = []
        for container in self.client.containers.list():
            if "{}-".format(instance_name) in container.name:
                instance_containers.append(container)
            
        self.__stopContainers(instance_containers)  


    # unused
    def deleteAllStoppedAppContainers(self):
        # TODO: exclude bibbox-sys-commander-* containers

        print("Removing stopped containers...")
        removed = self.client.containers.prune()
        if removed['ContainersDeleted']:
            print("Removed containers: {}".format([x for x in removed['ContainersDeleted']]))
        else:
            print("No containers to remove.")


    def deleteStoppedInstanceContainers(self, instance_name):
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

    