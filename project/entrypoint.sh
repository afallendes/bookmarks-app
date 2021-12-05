#!/bin/sh

# Make migrations for admin, auth, contenttypes, sessions apps
python manage.py makemigrations

# Make migrations for backend app
python manage.py makemigrations backend

# Migrate models
python manage.py migrate

# Run development server
python manage.py runserver 0.0.0.0:8000
