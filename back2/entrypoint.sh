#!/bin/bash
# Docker entrypoint script.

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
