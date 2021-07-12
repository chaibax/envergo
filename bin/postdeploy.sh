#!/bin/bash
# This script is ran by scalingo to start the application

echo "Deploying the EnvErgo Django app ($DJANGO_SETTINGS_MODULE)"
python manage.py migrate
python manage.py compilemessages -l fr -i .scalingo
python manage.py collectstatic --noinput
python manage.py compress --force