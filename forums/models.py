from django.db import models
from lesson.custom import UUID_field
from lesson.models import CustomUser

class NewsArticle(models.Model):
    """
    AI news that are fetched from news Api and seeded into db
    """
    id = UUID_field()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)  # Ensure no duplicate articles
    image_url = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Forum(models.Model):
    id = UUID_field()
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ForumThread(models.Model):
    id = UUID_field()
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE, related_name='threads'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

class ForumReply(models.Model):
    id = UUID_field()
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.created_by.username} on {self.thread.title}"


    