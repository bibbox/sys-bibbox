#!/bin/bash


sudo apt-get update

sudo apt-get install docker.io -y
sudo apt install nodejs npm -y
sudo apt install git -y
sudo apt install python3-pip -y
sudo apt-get install python3-venv -y

sudo npm i -g @angular/cli -n
python3 -m pip install virtualenv

sudo groupadd docker
sudo docker network create bibbox-default-network
sudo usermod -aG docker $USER
newgrp docker

cd /opt
sudo mkdir bibbox
sudo chmod -R 777 bibbox/
cd bibbox
mkdir instances
mkdir -p proxy/sites
mkdir config

git clone https://github.com/bibbox/sys-bibbox.git
cd sys-bibbox

python3 -m venv bibbox-venv
source bibbox-venv/bin/activate
cd backend
pip3 install -r requirements.txt
pip3 install docker-compose

cd ../frontend

ng analytics off
sudo npm i

cp /opt/bibbox/sys-bibbox/config-templates/100-error.conf /opt/bibbox/proxy/sites/100-error.conf
cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf /opt/bibbox/proxy/sites/000-default.conf
cp /opt/bibbox/sys-bibbox/config-templates/bibbox.config /opt/bibbox/config/bibbox.config
cp /opt/bibbox/sys-bibbox/config-templates/proxy-default.template /opt/bibbox/config/proxy-default.template

sudo `which docker-compose` up --build
sudo docker restart bibbox-sys-commander-backend