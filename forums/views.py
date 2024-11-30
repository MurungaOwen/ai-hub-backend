from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Forum, ForumThread, ForumReply
from .serializers import ForumSerializer, ForumThreadSerializer, ForumReplySerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .permissions import IsPremiumUser


class ForumListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForumSerializer
    queryset = Forum.objects.all()
    @swagger_auto_schema(
        tags=['Forum'],
        operation_summary="List Forums",
        operation_description="Lists all available forums",
        responses={200: ForumSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ForumThreadListCreateView(APIView):
    permission_classes = [IsPremiumUser]
    @swagger_auto_schema(
        tags=['Forum'],
        operation_summary="List Forum Threads",
        operation_description="Lists all threads in a specific forum",
        responses={200: ForumThreadSerializer(many=True)}
    )
    def get(self, request, forum_id):
        forum = get_object_or_404(Forum, id=forum_id)
        threads = ForumThread.objects.filter(forum=forum)
        serializer = ForumThreadSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Forum'],
        operation_summary="Create Forum Thread",
        operation_description="Create a new thread in a forum.",
        responses={201: ForumThreadSerializer},
    )
    def post(self, request, forum_id):
        forum = get_object_or_404(Forum, id=forum_id)
        serializer = ForumThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, forum=forum)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForumReplyListCreateView(APIView):
    permission_classes = [IsPremiumUser]

    @swagger_auto_schema(
        tags=['Forum'],
        operation_summary="List Replies",
        operation_description="Lists all replies for a specific thread",
        responses={200: ForumReplySerializer(many=True)}
    )
    def get(self, request, thread_id):
        thread = get_object_or_404(ForumThread, id=thread_id)
        replies = ForumReply.objects.filter(thread=thread)
        serializer = ForumReplySerializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Forum'],
        operation_summary="Create Reply",
        operation_description="Create a new reply to a thread",
        responses={201: ForumReplySerializer},
    )
    def post(self, request, thread_id):
        thread = get_object_or_404(ForumThread, id=thread_id)
        serializer = ForumReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumReplyDeleteView(APIView):
    permission_classes = [IsPremiumUser]

    @swagger_auto_schema(
        tags=['Forum'],
        operation_summary="Delete Reply",
        operation_description="Only the creator of the reply or an admin can delete the reply.",
        responses={
            204: openapi.Response(description="Reply deleted successfully."),
            403: openapi.Response(description="Permission denied."),
            404: openapi.Response(description="Reply not found."),
        }
    )
    def delete(self, request, pk):
        reply = get_object_or_404(ForumReply, id=pk)
        if reply.created_by == request.user or request.user.is_staff:
            reply.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "You do not have permission to delete this reply."},
                status=status.HTTP_403_FORBIDDEN
            )

