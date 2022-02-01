FROM httpd:latest

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

RUN apt-get -y update && \
    apt-get install -y certbot && \
    apt-get install -y python3-certbot-apache;

RUN certbot --apache -d ${DOMAINNAME:-demo.bibbox.org} -n --email ${EMAIL:-backoffice.bibbox@gmail.com} --agree-tos

# COPY htaccess.conf /var/www/html/sys-bibbox-client/.htaccess

EXPOSE 80
EXPOSE 443

CMD ["httpd", "-D", "FOREGROUND"]
