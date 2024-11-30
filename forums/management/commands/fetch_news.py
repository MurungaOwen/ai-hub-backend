import requests
from django.core.management.base import BaseCommand
from forums.models import NewsArticle
from datetime import datetime, timedelta
from decouple import config


class Command(BaseCommand):
    help = "Fetch AI news and seed into the database"

    def handle(self, *args, **kwargs):
        API_KEY = config('NEWS_API_KEY')
        NEWS_API_URL = "https://newsapi.org/v2/everything"
        QUERY = "artificial intelligence"

        response = requests.get(NEWS_API_URL, params={
            "q": QUERY,
            "apiKey": API_KEY,
            "pageSize": 40,  # Fetch up to 40 latest articles
        })

        if response.status_code == 200:
            articles = response.json().get("articles", [])
            count = 0
            for article in articles:
                published_at = article.get("publishedAt")
                try:
                    # Convert publishedAt to datetime
                    published_at_dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                    
                    # Create or update the article in the database
                    obj, created = NewsArticle.objects.update_or_create(
                        url=article.get("url"),
                        defaults={
                            "title": article.get("title"),
                            "description": article.get("description"),
                            "image_url": article.get("urlToImage"),
                            "published_at": published_at_dt,
                        }
                    )
                    if created:
                        count += 1
                except Exception as e:
                    self.stderr.write(f"Error saving article: {e}")
            
            self.stdout.write(f"Successfully added {count} new articles.")
        else:
            self.stderr.write(f"Failed to fetch news: {response.status_code} - {response.json().get('message', '')}")

        # Delete outdated news
        self.clean_outdated_news()

    def clean_outdated_news(self):
        retention_period = 20  #retain news if published 7 days ago
        threshold_date = datetime.now() - timedelta(days=retention_period)
        deleted_count, _ = NewsArticle.objects.filter(
            published_at__lt=threshold_date
        ).delete()
        self.stdout.write(f"Deleted {deleted_count} outdated news articles.")
