#!/bin/bash
: '
---------------------------------------------------------------------------------------------------
TODO: before running this script, run the following commands:

    sudo apt install git -y
    sudo apt-get install docker.io -y
    sudo docker network create bibbox-default-network
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker

    cd /opt
    sudo mkdir bibbox
    cd bibbox
    sudo git clone https://github.com/bibbox/sys-bibbox.git
    cd sys-bibbox
    sudo bash INSTALL.sh



INFO: if you want to manually change the URLs after installing:
    change baseurl in /opt/bibbox/sys-bibbox/config-templates/bibbox.config
    change urls in /opt/bibbox/sys-bibbox/config-templates/  *.conf files
    change urls in /opt/bibbox/proxy/sites *.conf files

INFO: The first time loading the applications tab of the website shows no applications, as then all appinfos and envparams get inserted into the db.


---------------------------------------------------------------------------------------------------
'
read -p "Specify domainname + TLD (e.g. silicolabv4.bibbox.org): " DOMAINNAME
# TODO: read envparams from file

#sudo chmod -R 777 /opt/bibbox/
cd /opt/bibbox
mkdir -p {instances,proxy/sites,config}

# change domainname
chmod -R 775 /opt/bibbox/sys-bibbox/config-templates
cd /opt/bibbox/sys-bibbox/config-templates
sed -e "s/§§BASEURL/$DOMAINNAME/g" bibbox.config.template > bibbox.config
sed -e "s/§§BASEURL/$DOMAINNAME/g" 000-default.conf.template > 000-default.conf
sed -e "s/§§BASEURL/$DOMAINNAME/g" 100-error.conf.template > 100-error.conf
sed -e "s/§§BASEURL/$DOMAINNAME/g" 005-fdp.conf.template > 005-fdp.conf

chmod -R 775 /opt/bibbox/sys-bibbox/apacheproxy
cd /opt/bibbox/sys-bibbox/apacheproxy
sed -e "s/§§SERVERNAME/$DOMAINNAME/g" httpd.conf.template > httpd.conf

chmod -R 775 /opt/bibbox/sys-bibbox/frontend/src/environments
cd /opt/bibbox/sys-bibbox/frontend/src/environments

sed -e "s/§§BASEURL/$DOMAINNAME/g;" environment.ts.template > environment.ts
sed -e "s/§§BASEURL/$DOMAINNAME/g;" environment.prod.ts.template > environment.prod.ts

cd /opt/bibbox/sys-bibbox/fdp-configs
sed -e "s/§§BASEURL/$DOMAINNAME/g" fdp.env.template > fdp.env


# replace the realm export template
sed -e "s/§§BASEURL/$DOMAINNAME/g;" /opt/bibbox/sys-bibbox/keycloak/realms/realm-export.json.template > /opt/bibbox/sys-bibbox/keycloak/realms/realm-export.json


# copy config templates to the actual destination
cp /opt/bibbox/sys-bibbox/config-templates/100-error.conf /opt/bibbox/proxy/sites/100-error.conf
cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf /opt/bibbox/proxy/sites/000-default.conf
cp /opt/bibbox/sys-bibbox/config-templates/bibbox.config /opt/bibbox/config/bibbox.config
cp /opt/bibbox/sys-bibbox/config-templates/005-fdp.conf /opt/bibbox/proxy/sites/005-fdp.conf

cp /opt/bibbox/sys-bibbox/config-templates/proxy-default.template /opt/bibbox/config/proxy-default.template
cp /opt/bibbox/sys-bibbox/config-templates/proxy-websocket.template /opt/bibbox/config/proxy-websocket.template


docker network create bibbox-default-network


cd /opt/bibbox/sys-bibbox

echo -e "\nRunning the frontend builder docker-compose...\n"
docker compose -f docker-compose_frontend_builder.yml up --build -d

printf "\nWaiting for the container to be ready, this might take a while..."

container_name=$(docker ps -a --format "{{.Names}}" | grep "angularenv") 

exitcode=$(docker wait $container_name)

if [ $exitcode = 0 ]; then
    printf "done.\n" 
    docker compose -f docker-compose.dev.yml up --build --remove-orphans -d
else
    printf "Building the frontend failed !\n"
    exit 1
fi

echo 'INSTALLATION COMPLETE'
exit 0
: '
If an error occurs after installing, run the following commands:

sudo docker exec -it bibbox-sys-commander-backend python manage.py recreate_db

sudo docker-compose stop
sudo docker-compose up --build
'
