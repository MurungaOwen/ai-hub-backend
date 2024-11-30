from django.db import models
from django.contrib.auth.models import AbstractUser
from .custom import UUID_field
from django.utils.timezone import now
from datetime import timedelta
# Create your models here.


class CustomUser(AbstractUser):
    is_premium = models.BooleanField(default=False)
    premium_expiry = models.DateTimeField(null=True, blank=True)


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'beginner'),
        ('intermediate', 'intermediate'),
        ('expert', 'expert'),
    )
    id = UUID_field()
    title = models.CharField(max_length=255)
    thumbnail = models.URLField()
    description = models.TextField(blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.title

class Module(models.Model):
    id = UUID_field()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    id = UUID_field()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    id = UUID_field()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(blank=False)

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    id = UUID_field()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) :
        return self.text

class UserCourseProgress(models.Model):
    id = UUID_field()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="course_progress")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="user_progress")
    completed_modules = models.PositiveIntegerField(default=0)
    total_modules = models.PositiveIntegerField()
    percent_complete = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}: {self.percent_complete}% completed"

    def update_progress(self):
        if self.total_modules > 0:
            self.percent_complete = (self.completed_modules / self.total_modules) * 100
            self.is_completed = self.percent_complete == 100
            self.save()

class UserModuleProgress(models.Model):
    id = UUID_field()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="lesson_progress")
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    quiz_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return "{} is complete:{} in {}".format(self.user, self.is_completed, self.module.title)

class UserQuizAttempt(models.Model):
    id = UUID_field()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)
    passed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.total_score}"


class UserQuizResponse(models.Model):
    id = UUID_field()
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField()

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_option.is_correct if self.selected_option else False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.text[:30]}: {'Correct' if self.is_correct else 'Wrong'}"
   
class Assignment(models.Model):
    id = UUID_field()
    title = models.CharField(max_length=255)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="module_assignments")
    text = models.TextField(max_length=255)

    def __str__(self) -> str:
        return self.title

class AssignmentSubmission(models.Model):
    id = UUID_field()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    files = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.TextField()
    instructor_feedback = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return "Assignment for: {} by : {}".format(self.assignment.title, self.user)
