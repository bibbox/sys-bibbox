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

##### Install the BiBBoX

`wget -O - https://raw.githubusercontent.com/bibbox/sys-bibbox/master/install.sh | bash`

## Use the BiBBoX via CLI

Run 

`bibbox -h`

for further help.

The available commands are:

`bibbox-installApp`
`bibbox-startApp`
`bibbox-stopApp`
`bibbox-copyApp`
`bibbox-listApps`
`bibbox-listInstalledApps`
`bibbox-removeApp`
`bibbox-getStatus`
`bibbox-startBibbox`
`bibbox-stopBibbox`

Use the flag -h or --help for a detailed app description.


A started app with a user defined instance name (instanceName) can be used under "localhost:8010/instanceName" in the browser.
