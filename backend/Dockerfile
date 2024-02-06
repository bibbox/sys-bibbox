FROM python:3.9.16

MAINTAINER Heimo Müller "heimo.mueller@mac.com"

ENV PYTHONUNBUFFERED 1
ENV CELERY_BROKER_URL       redis://redis:6379/0
ENV CELERY_RESULT_BACKEND   redis://redis:6379/0
ENV C_FORCE_ROOT true

RUN apt-get update

RUN apt-get install -y --force-yes \
    nasm \
    yasm

#
# FLASK SERVER
#

RUN mkdir -p /usr/src/bibbox-sys-commander
RUN mkdir /db_init_done
# Update working directory
WORKDIR  /usr/src/bibbox-sys-commander

# install all packages ...
COPY ./requirements.txt /usr/src/bibbox-sys-commander
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install the Docler CLI uswgi.ini
#ENV DOCKERVERSION=18.03.1-ce
#RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKERVERSION}.tgz \
#  && tar xzvf docker-${DOCKERVERSION}.tgz --strip 1 \
#                 -C /usr/local/bin docker/docker \
#  && rm docker-${DOCKERVERSION}.tgz

RUN curl -fsSL https://get.docker.com -o get-docker.sh
RUN sh get-docker.sh



COPY ./entrypoint.sh   /usr/src/bibbox-sys-commander
# Give execute permission to below file, so that the script can be executed by docker.
RUN chmod 777 /usr/src/bibbox-sys-commander/entrypoint.sh

COPY ./*.py            /usr/src/bibbox-sys-commander/
COPY ./uwsgi.*         /usr/src/bibbox-sys-commander/
COPY ./uwsgi.ini       /etc/uwsgi.ini
COPY ./.env            /usr/src/bibbox-sys-commander

EXPOSE 5000

# run server
CMD ["./entrypoint.sh"]

