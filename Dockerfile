FROM python:3.12-slim

WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    cron \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable to prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Copy the entrypoint script and cron jobs
COPY entrypoint.sh /app/entrypoint.sh
COPY jobs.cron /etc/cron.d/fetch_ai_news_cron

# Grant execution rights to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Apply cron jobs
RUN chmod 0644 /etc/cron.d/fetch_ai_news_cron
RUN crontab /etc/cron.d/fetch_ai_news_cron

# Expose the application port
EXPOSE 8000

# Start the entrypoint script
CMD ["./entrypoint.sh", "gunicorn", "ai_hub.wsgi:application", "--bind", "0.0.0.0:8000"]
