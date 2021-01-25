# BIBBOX COMMANDER

This directoy contains the BIBBOX COMMANDER (GUI and CLI for BB Version 4). 

## Quicktstart (for development)

`docker-compose build`

`docker-compose up -d`

`http://127.0.0.1:12000`

`http://127.0.0.1:12000/bibbox/api/docs/#/`

`http://127.0.0.1:12000/bibbox/api/v1/catalogues`

`http://127.0.0.1:12000/bibbox/api/v1/catalogues/active`

`http://127.0.0.1:12000/bibbox/api/v1/apps`

`http://127.0.0.1:12000/bibbox/api/v1/app_names`

`http://127.0.0.1:12000/bibbox/api/v1/users/`


## Within the Flask Server

`docker exec -it bibbox-sys-commander-backend /bin/bash`

## Debug Tools

### Celery Monitor 
`http://127.0.0.1:12000/bibbox/celerymon/`

### Adminer   
`http://127.0.0.1:8010/bibbox/adminer/`

### cadvisor
`http://127.0.0.1:8010/bibbox/cadvisor/`
* server postgres
* username postgres
* passpword postgres
* database bibbox


## Structure

##### client

##### backend

##### postgres

##### nginx

##### data

