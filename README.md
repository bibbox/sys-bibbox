# BiBBoX System

This container contains the BiBBoX [BIBBOX APP](http://bibbox.readthedocs.io/en/latest/admin-documentation/ "BIBBOX App Store"). 

## Initial Setup

To install the and use the bibbox software please follow these instructions:

##### Install Docker Engine

Run the following commands:

`sudo apt-get update`

`sudo apt -y install docker.io`

##### Install Docker Compose

To install the newest docker-compose package follow the insall dokumentation on the official docker website.

https://docs.docker.com/compose/install/

If you do not have installed the package curl, you can install it using 

`sudo apt-get -y install curl`

##### Clone GitHub Repository

Clone the BiBBoX repository to your prefered destination using the command

`git clone https://github.com/bibbox/sys-bibbox.git`

Change the direction to the sys-bibbox folder using

`cd sys-bibbox`

##### Create the BiBBoX default network

Run 

`sudo docker network create bibbox-default-network`

##### Start the nginx Webserver Container

Run 

`sudo docker-compose up -d`

## Test the BIBBOX

The bibbox backend is tested with Ubuntu 20.04, so it is recommendet to use this OS to run the BiBBoX.

Choose the folder "sys-bibbox" as working directory and run the predefined test script "test.py" with the command

`sudo python3 sys-backend/test.py`

The testfile contains predefined commands. For further testing it is recommented to open and modify the testfile or to run the specific commands in an IDE in debug mode.
