from rest_framework import generics, mixins
from .models import PaymentPlans
from .serializers import PaymentPlanSerializer
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ListPaymentPlans(generics.GenericAPIView, mixins.ListModelMixin):
    """
    List all available payment plans.
    """
    serializer_class = PaymentPlanSerializer
    queryset = PaymentPlans.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Payment'],
        operation_description="Retrieve a list of Payment plans",
        responses={200: openapi.Response('List of payment plans retrieved successfully', PaymentPlanSerializer(many=True))},
        operation_summary="List available payment plans"
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
list_payment_plans = ListPaymentPlans.as_view()