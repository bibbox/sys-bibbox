-- bibbox
CREATE DATABASE bibbox;

-- keycloak
CREATE DATABASE keycloak;
CREATE USER keycloak WITH ENCRYPTED PASSWORD 'keycloak';
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
\c keycloak postgres
GRANT ALL ON SCHEMA public TO keycloak;