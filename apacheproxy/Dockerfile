FROM ubuntu:22.04

MAINTAINER Heimo Müller "heimo.mueller@mac.com"

COPY httpd.conf /usr/local/apache2/conf/httpd.conf


RUN mkdir -p /usr/local/apache2/conf/sites/
RUN mkdir -p /var/www/html/sys-bibbox-client/
RUN mkdir -p /var/www/html/error/


COPY error.html /var/www/html/error/error.html
COPY robots.txt /var/www/robots.txt

# Install certbot
#RUN apt update && \
#   apt install -y snapd && \
#   snap install core && \
#  snap refresh core && \
#   snap install --classic certbot && \
#   ln -s /snap/bin/certbot /usr/bin/certbot;

#RUN apt-get -y update && \
#    apt-get install -y certbot && \
#    apt-get install -y python3-certbot-apache;

RUN apt-get -y update && \
    apt-get install -y apache2 && \
    a2enmod proxy_http && \
    a2enmod proxy_wstunnel && \
    a2enmod proxy_ajp && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y systemctl && \
    systemctl restart apache2 && \
#    service apache2 restart && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq install certbot && \
    apt-get install -y python3-certbot-apache;


#RUN certbot --apache -d ${DOMAINNAME:-demo.bibbox.org} -n --email ${EMAIL:-backoffice.bibbox@gmail.com} --agree-tos

# COPY htaccess.conf /var/www/html/sys-bibbox-client/.htaccess

EXPOSE 80
EXPOSE 443

#CMD ["httpd", "-D", "FOREGROUND"]
CMD ["tail", "-f", "/dev/null"]
