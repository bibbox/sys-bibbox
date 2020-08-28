#!/bin/bash

# mkdir opt/bibbox/bin
source mycommands.sh

mkdir -p apps
sudo chmod 777 apps
sudo chmod -R 777 conf

docker-compose up -d
