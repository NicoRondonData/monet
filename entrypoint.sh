#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      echo "Waiting for postgres... 558"

      sleep 0.1
    done

    echo "PostgreSQL started"
fi
ls -a
python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata data.json
exec "$@"
