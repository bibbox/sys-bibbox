# BiBBoX System

This container contains the BiBBoX [BIBBOX APP](http://bibbox.readthedocs.io/en/latest/admin-documentation/ "BIBBOX App Store"). 

* initial user/passwordd: **admin / admin**

## Initial Setup

To install the and use the bibbox software please follow these instructions:

##### Install Docker Engine

Run the following commands:

`sudo apt-get update`

`sudo apt install docker.io`

##### Install Docker Compose

To install the newest docker-compose package follow the insall dokumentation on the official docker website.

https://docs.docker.com/compose/install/

If you do not have installed the package curl, you can install it using `sudo apt-get install curl`.

##### Clone GitHub Repository

Clone the BiBBoX repository to your prefered destination using the command

`git clone https://github.com/bibbox/sys-bibbox.git`.

Change the direction to the sys-bibbox folder using

`cd sys-bibbox`

##### Start the nginx Webserver Container

Run `sudo docker-compose up -d`

##### Create the BiBBoX default network

Run `docker network create bibbox-default-network`.

## Test the BIBBOX

