#MAINTAINER Heimo Müller "heimo.mueller@mac.com"
FROM httpd:latest

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

RUN mkdir -p /usr/local/apache2/conf/sites/
RUN mkdir -p /var/www/html/sys-bibbox-client/
RUN mkdir -p /var/www/html/error/

COPY error.html /var/www/html/error/error.html
COPY robots.txt /var/www/robots.txt

EXPOSE 80

CMD ["httpd", "-D", "FOREGROUND"]
