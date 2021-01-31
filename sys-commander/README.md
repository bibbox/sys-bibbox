# BIBBOX COMMANDER

This directoy contains the BIBBOX COMMANDER (GUI and CLI for BB Version 4). 

## Quicktstart (for development)

`docker-compose build`
`docker-compose up -d`

`http://127.0.0.1:5000`


## Within the Flask Server

`docker exec -it bibbox-sys-commander-backend /bin/bash`

## Debug Tools

### Celery Monitor 
`http://127.0.0.1:5010`

### Adminer   
`http://127.0.0.1:5020`
* server postgres
* username postgres
* passpword postgres
* database bibbox

### cadvisor
`http://127.0.0.1:5030`


## Structure

##### client

##### backend

##### postgres

##### nginx

##### data

