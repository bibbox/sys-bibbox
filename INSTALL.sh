#!/bin/bash
: '
---------------------------------------------------------------------------------------------------
TODO: before running this script, run the following commands:

    sudo apt install git -y
    sudo apt-get install docker.io -y
    sudo docker network create bibbox-default-network
    sudo usermod -aG docker $USER
    newgrp docker

    cd /opt
    sudo mkdir bibbox
    cd bibbox
    sudo git clone https://github.com/bibbox/sys-bibbox.git
    cd sys-bibbox
    bash INSTALL.sh



INFO: if you want to manually change the URLs after installing:
    change api-url in /opt/bibbox/sys-bibbox/frontend/src/proxy.conf.json --> "target" : "NEW_API_URL" (e.g. "http://api.silicolabv4.bibbox.org)
    change baseurl in /opt/bibbox/sys-bibbox/config-templates/bibbox.config
    change urls in /opt/bibbox/sys-bibbox/config-templates/  *.conf files
    change urls in /opt/bibbox/proxy/sites *.conf files

INFO: The first time loading the applications tab of the website shows no applications, as then all appinfos and envparams get inserted into the db.


---------------------------------------------------------------------------------------------------
'
read -p "Specify domainname + TLD (e.g. silicolabv4.bibbox.org): " DOMAINNAME

sudo apt-get update
#sudo apt-get install docker.io -y
sudo apt install docker-compose -y
sudo apt install nodejs npm -y
sudo apt install python3-pip -y
printf 'n\n' | sudo npm i -g @angular/cli

#sudo chmod -R 777 /opt/bibbox/
cd /opt/bibbox
mkdir -p {instances,proxy/sites,config}

#sudo apt-get install python3-venv -y
#python3 -m venv bibbox-venv
#source bibbox-venv/bin/activate

cd /opt/bibbox/sys-bibbox/backend
pip3 install -r requirements.txt


cd /opt/bibbox/sys-bibbox/config-templates
sed -i -e "s/bibboxlocal/$DOMAINNAME/g" bibbox.config
sed -i -e "s/silicolabv4.bibboxlocal/$DOMAINNAME/g" 000-default.conf
sed -i -e "s/silicolabv4.bibboxlocal/$DOMAINNAME/g" 100-error.conf

cd /opt/bibbox/sys-bibbox/apacheproxy
sed -i -e "s/§§SERVERNAME/$DOMAINNAME/g" httpd.conf

cd /opt/bibbox/sys-bibbox/frontend/src
sed -i -e "s/silicolabv4.bibboxlocal/$DOMAINNAME/g" proxy.conf.json
sed -i -e "s/silicolabv4.bibboxlocal/$DOMAINNAME/g" app.config.ts


cd /opt/bibbox/sys-bibbox/frontend

printf 'n\n' | sudo npm i
sudo ng build --prod


cp /opt/bibbox/sys-bibbox/config-templates/100-error.conf /opt/bibbox/proxy/sites/100-error.conf
cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf /opt/bibbox/proxy/sites/000-default.conf
cp /opt/bibbox/sys-bibbox/config-templates/bibbox.config /opt/bibbox/config/bibbox.config
cp /opt/bibbox/sys-bibbox/config-templates/proxy-default.template /opt/bibbox/config/proxy-default.template


sudo docker-compose up --build -d
echo 'INSTALLATION COMPLETE'

: '
If an error occurs after installing, run the following commands:

sudo docker exec -it bibbox-sys-commander-backend python manage.py recreate_db
sudo docker exec -it bibbox-sys-commander-backend python manage.py seed_db
sudo docker-compose stop
sudo docker-compose up --build
'