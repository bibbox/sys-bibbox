#!/bin/bash

if [ -f "./frontend/dist/sys-bibbox-client/index.html" ]; then
    echo "Container Healthy"
    exit 0  # Success
else
    echo "Container not healthy"
    exit 1  # Failure
fi
