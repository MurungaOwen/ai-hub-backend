from django.urls import path
from .news_views import list_news
from .views import (
    ForumListView, ForumReplyDeleteView, ForumReplyListCreateView,
    ForumThreadListCreateView
)
urlpatterns = [
    path('news/', list_news, name="news"),
    path('forums/', ForumListView.as_view(), name='forum-list'),  # List Forums
    path('forums/<str:forum_id>/threads/', ForumThreadListCreateView.as_view(), name='forum-thread-list-create'),  # List and create thread
    path('forums/threads/<str:thread_id>/replies/', ForumReplyListCreateView.as_view(), name='forum-reply-list-create'),  # List and create reply
    path('threads/replies/<str:pk>/', ForumReplyDeleteView.as_view(), name='forum-reply-delete'),
]
