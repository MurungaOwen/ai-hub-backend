from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import NewsArticle, Forum, ForumThread, ForumReply

class NewsSerializer(ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = "__all__"
    
class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'title', 'description', 'created_at']

class ForumThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumThread
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
    

class ForumReplySerializer(serializers.ModelSerializer):
    written_by = serializers.SerializerMethodField()
    class Meta:
        model = ForumReply
        fields = ['id', 'content', 'written_by', 'created_at']
    
    def get_written_by(self, obj):
        return obj.created_by.username