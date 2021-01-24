# BIBBOX COMMANDER

This directoy contains the BIBBOX COMMANDER (GUI and CLI for BB Version 4). 

## Quicktstart (for development)

`docker-compose build`

`docker-compose up -d`

`http://127.0.0.1:20080/api/docs/#/`

`http://127.0.0.1:20080/api/v1/catalogues`

`http://127.0.0.1:20080/api/v1/catalogues/active`

`http://127.0.0.1:20080/api/v1/apps`

`http://127.0.0.1:20080/api/v1/app_names`

`http://127.0.0.1:20080/api/v1/users/`

## Within the Flask Server

`docker exec -it bibbox-sys-commander-backend /bin/bash`

## Debug Tools

### Celery Monitor 
`http://127.0.0.1:20083/tasks`

### Adminer / Postgres  
`http://127.0.0.1:20084`
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

