#!/bin/bash

# mkdir opt/bibbox/bin
source mycommands.sh

mkdir -p apps
sudo chmod 777 apps
sudo chmod -R 777 conf

sudo cp conf/userinput/runningContainers.json conf/userinput/runningContainerslocal.json
