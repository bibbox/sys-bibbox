FROM python:3.6.2

MAINTAINER Heimo Müller "heimo.mueller@mac.com"

ENV PYTHONUNBUFFERED 1
ENV CELERY_BROKER_URL       redis://redis:6379/0
ENV CELERY_RESULT_BACKEND   redis://redis:6379/0
ENV C_FORCE_ROOT true


RUN apt-get update

RUN apt-get install -y \
    nasm \
    yasm

#
# FLASK SERVER
#

RUN mkdir -p /usr/src/bibbox-sys-commander

# Update working directory
WORKDIR  /usr/src/bibbox-sys-commander

# copy everything from this directory to server/flask docker container
COPY ./requirements.txt /usr/src/bibbox-sys-commander
COPY ./entrypoint.sh   /usr/src/bibbox-sys-commander
COPY ./*.py      /usr/src/bibbox-sys-commander/
COPY ./uwsgi.*   /usr/src/bibbox-sys-commander/
COPY ./.env     /usr/src/bibbox-sys-commander

# Give execute permission to below file, so that the script can be executed by docker.
RUN chmod 777 /usr/src/bibbox-sys-commander/entrypoint.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY uswgi.ini
COPY ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

# run server
CMD ["./entrypoint.sh"]