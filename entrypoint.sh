#!/usr/bin/env bash

# start background tasks 
python manage.py process_tasks &

gunicorn --workers=3 myscraper.wsgi:application -b 0.0.0.0:8080