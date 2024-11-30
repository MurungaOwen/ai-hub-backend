from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserQuizAttempt, UserQuizResponse, Question, AnswerOption, Quiz
from .serializers import UserQuizAttemptSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .quiz_helper import complete_module_and_update_progress


class SubmitQuizMixin(APIView):
    """
    Mixin to handle quiz submission by users. This saves the user's quiz attempt,
    tracks their answers, and calculates their score.
    """
    permission_classes=[IsAuthenticated]

    def post(self, request, quiz_id):
        user = request.user
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Retrieve the answers submitted by the user
        quiz_answers = request.data.get("answers", [])

        if not quiz_answers:
            return Response({"detail": "No answers provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a quiz attempt record
        attempt = UserQuizAttempt.objects.create(user=user, quiz=quiz)

        total_score = 0
        for answer in quiz_answers:
            question = get_object_or_404(Question, id=answer.get("question_id"))
            selected_option = get_object_or_404(AnswerOption, id=answer.get("selected_option_id"))
            
            # Check if the answer is correct
            is_correct = selected_option.is_correct
            if is_correct:
                total_score += 1  # Assuming 1 point per correct answer
            
            # Save the user's response
            UserQuizResponse.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

        # Update the total score of the attempt
        attempt.total_score = total_score
        attempt.passed = total_score >= quiz.questions.count() / 2  # Assuming passing score is half of total questions
        attempt.save()
        passing_score = quiz.questions.count() / 2
        module_completed = False
        if attempt.passed:
            module_completed = complete_module_and_update_progress(
                user=user,
                module_id=quiz.module.id,
                quiz_score=total_score,
                passing_score=passing_score
            )

        return Response(
            {
                "attempt": UserQuizAttemptSerializer(attempt).data,
                "module_completed": module_completed,
            },
            status=status.HTTP_200_OK
        )