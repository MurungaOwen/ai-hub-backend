from drf_yasg.utils import swagger_auto_schema
from .custom_mixin import SubmitQuizMixin
from drf_yasg import openapi

class SubmitQuizView(SubmitQuizMixin):
    """
    Submit a quiz attempt and record user responses.
    """
    
    @swagger_auto_schema(
        tags=['Quiz'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "answers": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "question_id": openapi.Schema(
                                type=openapi.TYPE_STRING, 
                                description="UUID of the question"
                            ),
                            "selected_option_id": openapi.Schema(
                                type=openapi.TYPE_STRING, 
                                description="UUID of the selected answer option"
                            ),
                        },
                    ),
                )
            },
            required=["answers"],
            example={
                "answers": [
                    {"question_id": "7d6f89c7-0edb-48f1-9397-c6e2e0adf788", "selected_option_id": "1313a324-114f-46d1-adf4-47ea4a783bb9"},
                    {"question_id": "dd4aa3cb-e60e-402d-a8c0-6dafcc69d136", "selected_option_id": "c151b76b-e023-4478-a47e-47f8cdab30a7"}
                ]
            }
        ),
        responses={
            201: openapi.Response(
                description="Quiz submission successful",
                examples={
                    "application/json": {
                        "attempt_id": "a2b3c4d5-6e7f-8g9h-0i1j-2k3l4m5n6o7p",
                        "user": {
                            "id": 1,
                            "username": "johndoe",
                        },
                        "quiz": {
                            "id": "43f9242b-f9ed-4499-b6b4-b188251bae5d",
                            "title": "General Knowledge Quiz"
                        },
                        "total_score": 4,
                        "passed": True
                    }
                }
            ),
            400: openapi.Response(description="Bad request, e.g., missing answers"),
        }
    )
    def post(self, request, quiz_id):
        return super().post(request, quiz_id)
submit_quiz = SubmitQuizView.as_view()