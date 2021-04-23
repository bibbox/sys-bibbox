#!/bin/bash
: '
TODO before running this script:
cd /opt
sudo mkdir bibbox
sudo apt install git -y
cd bibbox
sudo git clone https://github.com/bibbox/sys-bibbox.git
'
read -p "enter domainname (e.g. bibbox.org): " DOMAINNAME

sudo apt-get update
sudo apt-get install docker.io -y
sudo apt install docker-compose -y
sudo apt install nodejs npm -y
sudo apt install python3-pip -y
printf 'n\n' | sudo npm i -g @angular/cli

printf '\n' | sudo docker network create bibbox-default-network
sudo usermod -aG docker $USER
newgrp docker

sudo chmod -R 777 /opt/bibbox/
cd /opt/bibbox
mkdir -p {instances,proxy/sites,config}

#sudo apt-get install python3-venv -y
#python3 -m venv bibbox-venv
#source bibbox-venv/bin/activate

cd /opt/bibbox/sys-bibbox/backend
pip3 install -r requirements.txt

cd /opt/bibbox/sys-bibbox/frontend

printf 'n\n' | sudo npm i
sudo ng build --prod


cd /opt/bibbox/sys-bibbox/config-templates
sed -i -e "s/bibboxlocal/$DOMAINNAME/g" bibbox.config

cd /opt/bibbox/sys-bibbox/frontend/src
sed -i -e "s/bibboxlocal/$DOMAINNAME/g" proxy.conf.json



cp /opt/bibbox/sys-bibbox/config-templates/100-error.conf /opt/bibbox/proxy/sites/100-error.conf
cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf /opt/bibbox/proxy/sites/000-default.conf
cp /opt/bibbox/sys-bibbox/config-templates/bibbox.config /opt/bibbox/config/bibbox.config
cp /opt/bibbox/sys-bibbox/config-templates/proxy-default.template /opt/bibbox/config/proxy-default.template

#sudo `which docker-compose` stop
#sudo `which docker-compose` up

sudo docker-compose build
sudo docker-compose up



