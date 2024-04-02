import docker
import subprocess

class DockerHandler():

    def __init__(self):
        self.client = docker.from_env()
        self.INSTANCEPATH = "/opt/bibbox/instances/"


    def docker_stopInstance(self, instance_name):
        command = "docker compose stop".split()
        subprocess.call(command, cwd=f"{self.INSTANCEPATH}{instance_name}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")

    def docker_startInstance(self, instance_name):   
        command = "docker compose start".split()
        subprocess.call(command, cwd=f"{self.INSTANCEPATH}{instance_name}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")

    def docker_restartInstance(self, instance_name):   
        command = "docker compose restart".split()
        subprocess.call(command, cwd=f"{self.INSTANCEPATH}{instance_name}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
    

    def docker_getContainerLogs(self, instance_name):
        instance_name = str(instance_name).lower()
        container_logs_dict = {}
        containers = self.client.containers.list(filters={"label":["com.docker.compose.project={}".format(instance_name)]}, all=True)
        
        for container in containers:
            container_logs_dict[container.name] = str(container.logs(tail=200))[2:-1].split('\\n')

            ## subprocess implementation
            # command = 'docker logs {} --tail 200'.format(container.name).split()
            # process = subprocess.run(command, capture_output=True)
            # logs_from_container = process.stderr

            # container_logs_dict[container.name] = logs_from_container.split('\n')
        
        return container_logs_dict
    
    def docker_getSysContainerLogs(self, sys_container_name: str, tail=200):
        cname = str(sys_container_name).lower()
        container_logs_dict = {}

        containers = self.client.containers.list(filters={"name":cname}, all=False)


        container_logs_dict['name'] = sys_container_name
        container_logs_dict['tail'] = tail
        container_logs_dict['logs'] = str(containers[0].logs(tail=tail))[2:-1].split('\\n')

        return container_logs_dict


    def docker_getContainerNames(self, prefix):
        containers = self.client.containers.list(filters={"label":["com.docker.compose.project={}".format(prefix)]}, all=True)
        return [container.name for container in containers]

    def docker_deleteStoppedInstance(self, instance_name):
        command = "docker compose down".split()
        subprocess.call(command, cwd=f"{self.INSTANCEPATH}{instance_name}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")


        # removed = self.client.containers.prune(filters={"label":["com.docker.compose.project={}".format(instance_name)]})
        # status = ""
        # if removed['ContainersDeleted']:
        #     status = "Removed containers: {}".format([x for x in removed['ContainersDeleted']])
        #     print(status)
        # else:
        #     status = "No containers to remove."
        #     print(status)
    

    # def __stopContainers(self, containers):
    #     for container in containers:
    #         print("Stopping container: {}...  ".format(container.name), end="")
    #         container.stop()
    #         print("Stopped container: {}.\n".format(container.name))    

    
