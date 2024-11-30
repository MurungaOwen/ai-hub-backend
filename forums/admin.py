from django.contrib import admin
from .models import NewsArticle
from .models import Forum, ForumThread, ForumReply

class ForumAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at'] 
    search_fields = ['title'] 
    list_filter = ['created_at']
    ordering = ['-created_at']

class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'forum', 'title', 'created_by', 'created_at', 'updated_at']
    search_fields = ['title']
    list_filter = ['forum', 'created_at']
    ordering = ['-created_at'] 
    raw_id_fields = ['created_by']


class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread', 'created_by', 'created_at']
    search_fields = ['created_by__username', 'thread__title'] 
    list_filter = ['thread', 'created_at'] 
    ordering = ['-created_at']  
    raw_id_fields = ['created_by'] 


admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumThread, ForumThreadAdmin)
admin.site.register(ForumReply, ForumReplyAdmin)

admin.site.register(NewsArticle)