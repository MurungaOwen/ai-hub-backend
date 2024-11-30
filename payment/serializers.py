from rest_framework import serializers
from .models import PaymentPlans


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlans
        fields = "__all__"