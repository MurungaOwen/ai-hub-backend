from rest_framework import serializers
from .models import (
    Course, Module, Quiz, Question, 
    AnswerOption, Assignment, UserQuizAttempt, 
    UserQuizResponse, UserCourseProgress, UserModuleProgress, 
    CustomUser
)

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    question_options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'question_options']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'module', 'title']

class CourseSerializer(serializers.ModelSerializer):
    total_modules = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'title', 'total_modules', 'thumbnail', 'description', 'is_premium', 'level']
    
    def get_total_modules(self, obj):
        return obj.modules.count()

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

class ModuleDetailedSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)
    module_assignments = serializers.StringRelatedField(many=True, read_only=True)  # Assuming we have simple string representations

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'video_url', 'quizzes', 'module_assignments']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'text']


class UserCourseProgressSerializer(serializers.ModelSerializer):
    course_details = serializers.SerializerMethodField()
    class Meta:
        model = UserCourseProgress
        fields = ['id', 'course_details', 'completed_modules', 'total_modules', 'percent_complete', 'is_completed', 'last_accessed']

    def get_course_details(self, obj):
        """get details of the course"""
        completed_modules = UserModuleProgress.objects.filter(
            user=obj.user,
            module__course=obj.course, 
            is_completed=True
        ).values_list('module__id', flat=True)

        return {
            "title": obj.course.title,
            "course_id": obj.course.id,
            "completed_modules_id": list(completed_modules)
        }

class UserModuleProgressSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta:
        model = UserModuleProgress
        fields = ['id', 'user', 'course', 'module', 'is_completed', 'quiz_score']
    def get_course(self, obj):
        return obj.module.course

class UserQuizAttemptSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    quiz = serializers.CharField(source="quiz.title")
    responses = serializers.SerializerMethodField()

    class Meta:
        model = UserQuizAttempt
        fields = ['id', 'user', 'quiz', 'total_score', 'passed', 'attempted_at', 'responses']

    def get_responses(self, obj):
        responses = UserQuizResponse.objects.filter(attempt=obj)
        return UserQuizResponseSerializer(responses, many=True).data

class UserQuizResponseSerializer(serializers.ModelSerializer):
    question_id = serializers.CharField(source="question.id")
    is_correct = serializers.BooleanField()

    class Meta:
        model = UserQuizResponse
        fields = ['question_id', 'is_correct']

class UserSerializer(serializers.ModelSerializer):
    subscription_end = serializers.SerializerMethodField()
    current_plan = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_premium', 'subscription_end', 'current_plan']
    
    def get_subscription_end(self, obj):
        if obj.is_premium:
            return obj.customer.subscription_end
        return None
        
    
    def get_current_plan(self, obj):
        if obj.is_premium:
            return {
                "id": obj.customer.current_plan.id,
                "name": obj.customer.current_plan.name
            }
        return None