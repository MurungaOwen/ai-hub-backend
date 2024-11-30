from django.urls import path
from .course_view import list_courses, course_detail, list_quiz_questions
from .views import submit_quiz
from .user_view import user_course_progress, user_info
urlpatterns = [
    path('courses/', list_courses, name="courses"),
    path('user/progress/', user_course_progress),
    path('user/', user_info),
    path('course/<str:pk>/', course_detail, name="course_detail"),
    path('quiz/<str:quiz_id>/questions/', list_quiz_questions, name='quiz-questions-list'),
    path('quiz/<str:quiz_id>/submit/', submit_quiz, name='submit_quiz_attempt'),
]
