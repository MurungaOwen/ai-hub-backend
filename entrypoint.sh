#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations

echo "migrating..."
python manage.py migrate

# Run seeders (or any custom commands)
echo "Running seeders..."
python manage.py seed_courses

echo "Creating admin user"
python manage.py create_admin

echo "seeding forums"
python manage.py add_forums

# Collect static files (for production)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start cron service
echo "Starting cron service..."
service cron start

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn ai_hub.wsgi:application --bind 0.0.0.0:8000
