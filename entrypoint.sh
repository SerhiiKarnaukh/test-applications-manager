#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python /usr/src/app/shop/manage.py flush --no-input
python /usr/src/app/shop/manage.py migrate

exec "$@"
