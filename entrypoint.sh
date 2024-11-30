#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the cron service
echo "Starting cron service..."
service cron start


echo "Starting Gunicorn server..."
exec "$@"
