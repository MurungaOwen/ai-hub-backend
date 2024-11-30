from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from .serializers import NewsSerializer
from .models import NewsArticle
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ListNews(generics.GenericAPIView, mixins.ListModelMixin):
    """
    List all latest AI news
    """
    serializer_class = NewsSerializer
    queryset = NewsArticle.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['News'],
        operation_description="Retrieve a list of latest AI news",
        responses={200: openapi.Response('List of News retrieved successfully', NewsSerializer(many=True))},
        operation_summary="Latest AI news"
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
list_news = ListNews.as_view()
