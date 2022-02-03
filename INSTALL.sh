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
read -p "Specify EMAIL for https-certificate (e.g. backoffice.bibbox@gmail.com): " EMAIL
# TODO: read envparams from file

wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" bash_completion

nvm install 14.16.0
nvm use v14.16.0

apt-get update
#apt-get install docker.io -y
apt install docker-compose -y
apt install npm -y
apt install python3-pip -y

#nvm install 14.16.0 -y
#printf 'n\n' | npm i -g @angular/cl
#npm audit fix
#printf 'n\n' | npm i -g

#printf 'n\n' | npm update -g @angular/cli


#sudo chmod -R 777 /opt/bibbox/
cd /opt/bibbox
mkdir -p {instances,proxy/sites,config}

#sudo apt-get install python3-venv -y
#python3 -m venv bibbox-venv
#source bibbox-venv/bin/activate

cd /opt/bibbox/sys-bibbox/backend
pip3 install -r requirements.txt



# change domainname
chmod -R 775 /opt/bibbox/sys-bibbox/config-templates
cd /opt/bibbox/sys-bibbox/config-templates
sed -e "s/§§BASEURL/$DOMAINNAME/g" bibbox.config.template > bibbox.config
sed -e "s/§§BASEURL/$DOMAINNAME/g" 000-default.conf.template > 000-default.conf
sed -e "s/§§BASEURL/$DOMAINNAME/g" 100-error.conf.template > 100-error.conf

chmod -R 775 /opt/bibbox/sys-bibbox/apacheproxy
cd /opt/bibbox/sys-bibbox/apacheproxy
sed -e "s/§§SERVERNAME/$DOMAINNAME/g" httpd.conf.template > httpd.conf

chmod -R 775 /opt/bibbox/sys-bibbox/frontend/src/environments
cd /opt/bibbox/sys-bibbox/frontend/src/environments
sed -e "s/§§BASEURL/$DOMAINNAME/g" environment.ts.template > environment.ts
sed -e "s/§§BASEURL/$DOMAINNAME/g" environment.prod.ts.template > environment.prod.ts


# compile frontend code
cd /opt/bibbox/sys-bibbox/frontend

printf 'n\n' | npm i
#printf 'n\n' | npm update

ng build --prod


# copy config templates to the actual destination
cp /opt/bibbox/sys-bibbox/config-templates/100-error.conf /opt/bibbox/proxy/sites/100-error.conf
cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf /opt/bibbox/proxy/sites/000-default.conf
cp /opt/bibbox/sys-bibbox/config-templates/bibbox.config /opt/bibbox/config/bibbox.config

cp /opt/bibbox/sys-bibbox/config-templates/proxy-default.template /opt/bibbox/config/proxy-default.template
cp /opt/bibbox/sys-bibbox/config-templates/proxy-websocket.template /opt/bibbox/config/proxy-websocket.template


docker-compose up --build -d

docker exec -it bibbox-sys-commander-apacheproxy certbot --apache -d ${DOMAINNAME:-demo.bibbox.org} -n --email ${EMAIL:-backoffice.bibbox@gmail.com} --agree-tos

docker exec -it bibbox-sys-commander-apacheproxy cp /usr/local/apache2/conf/sites/000-default.conf /etc/apache2/sites-available/000-default-le-ssl.conf

docker exec -it bibbox-sys-commander-apacheproxy systemctl restart apache2


# re init db
# docker exec bibbox-sys-commander-backend python manage.py recreate_db
# docker exec bibbox-sys-commander-backend python manage.py seed_db


echo 'INSTALLATION COMPLETE'

: '
If an error occurs after installing, run the following commands:

sudo docker exec -it bibbox-sys-commander-backend python manage.py recreate_db
sudo docker exec -it bibbox-sys-commander-backend python manage.py seed_db
sudo docker-compose stop
sudo docker-compose up --build
'
