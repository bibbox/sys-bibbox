import docker
import subprocess

class DockerHandler():

    def __init__(self):
        self.client = docker.from_env()
        self.INSTANCEPATH = "/opt/bibbox/instances/"


    def docker_stopInstance(self, instance_name):
        command = "docker-compose stop".split()
        subprocess.call(command, cwd=f"{self.INSTANCEPATH}{instance_name}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")

    def docker_startInstance(self, instance_name):   
        command = "docker-compose start".split()
        subprocess.call(command, cwd=f"{self.INSTANCEPATH}{instance_name}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")

    def docker_restartInstance(self, instance_name):   
        command = "docker-compose restart".split()
        subprocess.call(command, cwd=f"{self.INSTANCEPATH}{instance_name}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")

    def docker_exec(self,instance_name,command_array):
        #logger.info("subprocess: {command}".format(command=" ".join(command_array)))
        docker_command=['docker', 'exec', instance_name]
        docker_command.extend(command_array)
        process = subprocess.Popen(docker_command,
                                   shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
        std_out=[]
        std_error=[]
        while True:
            line = process.stdout.readline()
            lineerror = process.stderr.readline()
            if not line and not lineerror:
                break
            if line:
                std_out.appand(line.rstrip())
            if lineerror:
                std_out.appand(lineerror.rstrip())

        return {"std_out":std_out,
                "std_error":std_error}

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

    def docker_deleteStoppedInstance(self, instance_name):
        command = "docker-compose down".split()
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

    
