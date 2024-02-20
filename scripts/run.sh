#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 1 --master --threads 4 --module portfolio.wsgi &
gunicorn --bind 0.0.0.0:8000 portfolio.asgi -w 1 --threads 4 -k uvicorn.workers.UvicornWorker
