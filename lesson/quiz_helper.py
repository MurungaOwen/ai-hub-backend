from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Module, UserModuleProgress, UserCourseProgress


def complete_module_and_update_progress(user, module_id, quiz_score, passing_score):
    """
    Marks a module as completed if the user passes the quiz.
    Updates course progress accordingly.
    """
    module = get_object_or_404(Module, id=module_id)
    course = module.course

    
    user_module_progress, created = UserModuleProgress.objects.get_or_create(
        user=user,
        module=module,
        defaults={"quiz_score": quiz_score}
    )

    if not user_module_progress.is_completed and quiz_score >= passing_score:
        user_module_progress.is_completed = True
        user_module_progress.quiz_score = quiz_score
        user_module_progress.save()

        # Update UserCourseProgress
        user_course_progress, created = UserCourseProgress.objects.get_or_create(
            user=user,
            course=course,
            defaults={"total_modules": course.modules.count()}
        )

        # Increment completed modules
        user_course_progress.completed_modules += 1
        user_course_progress.update_progress()

        return True  # Module completed successfully
    return False  # Module not completed (quiz not passed)
