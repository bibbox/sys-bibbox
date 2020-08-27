#!/bin/bash

# mkdir opt/bibbox/bin
source mycommands.sh

mkdir -p apps
sudo chmod 777 apps

sudo cp conf/userinput/runningContainers.json conf/userinput/runningContainerslocal.json
