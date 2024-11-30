#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding courses.."
python manage.py seed_courses

echo "Adding forums..."
python manage.py add_forums

echo "fetch ai news.."
python manage.py fetch_news

echo "Creating admin .."
python manage.py create_admin


# Start the cron service
echo "Starting cron service..."
service cron start


echo "Starting Gunicorn server..."
exec "$@"
