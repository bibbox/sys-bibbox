FROM httpd:latest

MAINTAINER Heimo Müller "heimo.mueller@mac.com"

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

RUN mkdir -p /usr/local/apache2/conf/sites/
RUN mkdir -p /var/www/html/sys-bibbox-client/
RUN mkdir -p /var/www/html/error/


COPY index.html /ver/www/html/error/index.html
# COPY htaccess.conf /var/www/html/sys-bibbox-client/.htaccess

EXPOSE 80

CMD ["httpd", "-D", "FOREGROUND"]
