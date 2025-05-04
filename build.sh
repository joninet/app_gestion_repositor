#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating staticfiles directory..."
mkdir -p gestion/staticfiles

echo "Collecting static files..."
cd gestion
python manage.py collectstatic --noinput
