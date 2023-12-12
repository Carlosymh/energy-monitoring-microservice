#!/bin/bash
echo "Create migrations"
python manage.py makemigrations CRUD
echo "=============================="

echo "migrate"
python manage.py migrate
echo "=============================="

echo "Start Server"
python manage.py runserver 0.0.0.0:8000
