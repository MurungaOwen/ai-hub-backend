from django.contrib import admin
from .models import (
    CustomUser, Course, Module,
    Quiz, Question, AnswerOption,
    UserQuizAttempt, UserQuizResponse,
    UserCourseProgress, UserModuleProgress,
    Assignment, AssignmentSubmission
)


# CustomUser admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_premium', 'premium_expiry')
    list_filter = ('is_premium',)
    search_fields = ('username', 'email')

# Course admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'is_premium')
    list_filter = ('level', 'is_premium')
    search_fields = ('title', 'description')

# Module admin
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'description')
    list_filter = ('course',)

# Quiz admin
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')
    search_fields = ('title',)
    list_filter = ('module',)

# Question admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)
    list_filter = ('quiz',)

# AnswerOption admin
@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question')
    search_fields = ('text',)
    list_filter = ('is_correct', 'question')

# UserCourseProgress admin
@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'percent_complete', 'is_completed')
    list_filter = ('is_completed', 'course')
    search_fields = ('user__username', 'course__title')
    readonly_fields=['is_completed', 'percent_complete']

# UserModuleProgress admin
@admin.register(UserModuleProgress)
class UserModuleProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'is_completed', 'quiz_score')
    list_filter = ('is_completed', 'module')
    search_fields = ('user__username', 'module__title')
    readonly_fields = ['is_completed', 'quiz_score']

# UserQuizAttempt admin
@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'total_score', 'passed', 'attempted_at')
    list_filter = ('passed', 'quiz')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields =['passed', 'total_score']
# UserQuizResponse admin
@admin.register(UserQuizResponse)
class UserQuizResponseAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct')
    list_filter = ('is_correct', 'question')
    search_fields = ('attempt__user__username', 'question__text')
    readonly_fields =['is_correct']
# Assignment admin
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')
    search_fields = ('title', 'text')
    list_filter = ('module',)

# AssignmentSubmission admin
@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'user', 'submitted_at', 'grade')
    search_fields = ('assignment__title', 'user__username')
    list_filter = ('assignment', 'submitted_at')
