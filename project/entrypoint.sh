#!/bin/sh

# Remove previous migration files if any
rm */migrations/*.py

# Make migrations for admin, auth, contenttypes, sessions apps
python manage.py makemigrations

# Make migrations for backend app
python manage.py makemigrations backend

# Migrate models
python manage.py migrate

# Creates superuser from environment variables
python manage.py createsuperuser --noinput

# Run development server
python manage.py runserver 0.0.0.0:8000
