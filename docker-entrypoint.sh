#!/bin/bash
set -e

echo "Starting migrations"
sleep 2m
rm -rf migrations
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python run.py

exec "$@"
