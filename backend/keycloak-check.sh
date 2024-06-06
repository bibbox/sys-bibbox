#!/bin/bash

# Function to check if the URL gives a 200 status
check_url() {
    status_code=$(curl --head --write-out '%{http_code}' --silent --output /dev/null -fsS http://bibbox-sys-commander-keycloak:8080/realms/master)
    if [ "$status_code" -eq 200 ]; then
        return 1
    else
        return 0
        
    fi
}

# Wait until the URL gives a 200 status
while check_url; do
    echo "Waiting for keycloak..."
    sleep 5
done

exec /usr/src/bibbox-sys-commander/entrypoint.sh