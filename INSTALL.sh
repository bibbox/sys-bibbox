#!/bin/bash
: '
TODO before running this script:
cd /opt
sudo mkdir bibbox
sudo apt install git -y

git clone https://github.com/bibbox/sys-bibbox.git
cd sys-bibbox


'
sudo apt-get update
sudo apt-get install docker.io -y
sudo apt install nodejs npm -y
sudo apt install git -y
sudo apt install python3-pip -y
sudo apt-get install python3-venv -y
sudo npm i -g @angular/cli -n
export NG_CLI_ANALYTICS="false"

python3 -m pip install virtualenv

sudo groupadd docker
sudo docker network create bibbox-default-network
sudo usermod -aG docker $USER
newgrp docker

sudo chmod -R 777 /opt/bibbox/
cd /opt/bibbox
mkdir instances
mkdir -p proxy/sites
mkdir config

python3 -m venv bibbox-venv
source bibbox-venv/bin/activate
cd backend
pip3 install -r requirements.txt
pip3 install docker-compose

cd ../frontend

ng analytics off
sudo npm i
sudo ng build --prod

cp /opt/bibbox/sys-bibbox/config-templates/100-error.conf /opt/bibbox/proxy/sites/100-error.conf
cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf /opt/bibbox/proxy/sites/000-default.conf
cp /opt/bibbox/sys-bibbox/config-templates/bibbox.config /opt/bibbox/config/bibbox.config
cp /opt/bibbox/sys-bibbox/config-templates/proxy-default.template /opt/bibbox/config/proxy-default.template

sudo `which docker-compose` build
sudo `which docker-compose` up --no-start
docker start bibbox-sys-commander-backend bibbox-sys-commander-postgres
docker exec -it bibbox-sys-commander-backend python manage.py recreate_db

sudo `which docker-compose` stop
sudo `which docker-compose` up
