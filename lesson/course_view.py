from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Course, Module, Quiz
from django.shortcuts import get_object_or_404
from .serializers import CourseSerializer, QuestionSerializer, ModuleDetailedSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CourseDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    Retrieve a detailed view of a single course, including modules.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Courses'],
        operation_description="Retrieve detailed information about a course, including its modules.",
        responses={200: openapi.Response('Course details retrieved successfully', CourseSerializer)},
        operation_summary="Get course details and modules"
    )
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseSerializer(course)
        modules = Module.objects.filter(course=course)
        module_serializer = ModuleDetailedSerializer(modules, many=True)
        return Response({
            'course': serializer.data,
            'modules': module_serializer.data
        })
course_detail = CourseDetailView.as_view()


class ListCourses(generics.GenericAPIView, mixins.ListModelMixin):
    """
    List all available courses with optional filtering for premium/non-premium courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']

    @swagger_auto_schema(
        tags=['Courses'],
        operation_description="Retrieve a list of courses with optional filters for premium/non-premium.",
        responses={200: openapi.Response('List of courses retrieved successfully', CourseSerializer(many=True))},
        operation_summary="List available courses"
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
list_courses = ListCourses.as_view()

class QuizQuestionsListAPIView(generics.ListAPIView):
    """
    Retrieve all questions and answers for a specific quiz.
    """
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return quiz.questions.all()

    @swagger_auto_schema(
        tags=['Quiz'],
        manual_parameters=[
            openapi.Parameter(
                'quiz_id',
                openapi.IN_PATH,
                description="UUID of the quiz",
                type=openapi.TYPE_STRING,
                required=True,
            )

        ],
        responses={
            200: openapi.Response(
                description="List of questions and answers for the quiz",
                schema=QuestionSerializer(many=True)
            ),
            404: openapi.Response(
                description="Quiz not found"
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
list_quiz_questions = QuizQuestionsListAPIView.as_view()
