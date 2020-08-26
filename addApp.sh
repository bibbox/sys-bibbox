#!/bin/bash

echo Wich App you want to install?

read appName

cd apps

git clone https://github.com/bibbox/$appName.git

python3 setproxy.py

cd $appName

docker-compose up-d
