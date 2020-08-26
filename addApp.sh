#!/bin/bash

echo Wich App you want to install?

read appName

git clone https://github.com/bibbox/$appName.git

python3 setproxy.py

cd apps/$appName

docker-compose up-d
