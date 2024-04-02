#!/bin/sh

# Below shells script is required because the flask container need to wait for postgres db server to startup before
# accessing it below.


# TODO - for production take the password from the .env

USER=postgres
DATABASE=bibbox
HOST=postgres
if [ -z "${SKIP_RECREATE_DB}" ]; then
  SKIPPING_RECREATE_DB=false
else
  SKIPPING_RECREATE_DB=${SKIP_RECREATE_DB}
fi

echo "PostgreSQL started!"

# Run below commands from manage.py to initialize db and have some default data.
# add a flag to preserve the DB at a build
if [ ! -f  DBINIT.DONE ]; then
    if [ "$SKIPPING_RECREATE_DB" = true ]; then
      echo "Skipping recreate_db!!! SET SKIP_RECREATE_DB to false if you do not want to skip recreate_db"
    else
      python manage.py recreate_db
    fi
    python manage.py sync_app_catalogue
    touch /db_init_done/DBINIT.DONE
fi


# test if the db is working
# python manage.py



uwsgi --ini /etc/uwsgi.ini


# THIS is the websockets try
# python runflask.py
