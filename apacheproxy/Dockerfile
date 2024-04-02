FROM httpd:latest

#MAINTAINER Heimo Müller "heimo.mueller@mac.com"

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

#RUN apt-get update
#RUN apt-get install apache2 apache2-utils

RUN mkdir -p /usr/local/apache2/conf/sites/
RUN mkdir -p /var/www/html/sys-bibbox-client/
RUN mkdir -p /var/www/html/error/


COPY error.html /var/www/html/error/error.html
COPY robots.txt /var/www/robots.txt

EXPOSE 80

CMD ["httpd", "-D", "FOREGROUND"]
