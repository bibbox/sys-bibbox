#!/bin/bash

docker-compose down

rm /opt/bibbox/proxy/sites/000-default-le-ssl.conf
cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf.apache2 /opt/bibbox/proxy/sites/000-default.conf

docker-compose up --build -d

docker exec bibbox-sys-commander-apacheproxy ln -s ../sites-available/000-default.conf /etc/apache2/sites-enabled/


docker exec -it bibbox-sys-commander-apacheproxy certbot --apache -d ${DOMAINNAME:-demo.bibbox.org} -n --email ${EMAIL:-backoffice.bibbox@gmail.com} --agree-tos

cp /opt/bibbox/sys-bibbox/config-templates/000-default.conf /opt/bibbox/proxy/sites/000-default-le-ssl.conf

for proxy_conf_file in /opt/bibbox/proxy/sites/005*
do
  name=$(basename $proxy_conf_file)
  docker exec bibbox-sys-commander-apacheproxy ln -s ../sites-available/${name} /etc/apache2/sites-enabled/
  docker exec bibbox-sys-commander-apacheproxy certbot --expand --apache -d ${name}.${DOMAINNAME:-demo.bibbox.org} -n --email ${EMAIL:-backoffice.bibbox@gmail.com} --agree-tos
done

#docker exec -it bibbox-sys-commander-apacheproxy cp /usr/local/apache2/conf/sites/000-default.conf /etc/apache2/sites-available/000-default-le-ssl.conf

docker exec -it bibbox-sys-commander-apacheproxy apache2ctl -k graceful
