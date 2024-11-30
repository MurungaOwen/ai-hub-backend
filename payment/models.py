from django.db import models
from lesson.custom import UUID_field
from lesson.models import CustomUser


class PaymentPlans(models.Model):
    """plans that are avilable"""
    DURATION_CHOICES = (
        ('weekly', 'weekly'),
        ('annualy', 'annualy'),
        ('monthly', 'monthly'),
    )
    id = UUID_field()
    stripe_price_id = models.CharField(max_length=200, null=True, blank=True)
    stripe_product_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    duration = models.CharField(max_length=20, choices = DURATION_CHOICES)
    features = models.TextField()

class StripeCustomers(models.Model):
    CUSTOMER_STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('canceled', 'canceled'),
        ('expired', 'expired'),
        ('past_due', 'past_due')
    )
    id = UUID_field()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer', null=True)
    stripe_customer_id = models.CharField(max_length=200)
    current_plan = models.ForeignKey(PaymentPlans, on_delete=models.SET_NULL, related_name="plan", null=True)
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CUSTOMER_STATUS_CHOICES, default='inactive')

class PaymentTransaction(models.Model):
    """The payment for a course"""
    STATUS_CHOICES = (
        ('success', 'success'),
        ('failed', 'failed'),
        ('pending', 'pending')
    )
    id = UUID_field()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    currency = models.CharField(max_length=5)
    payment_plan = models.ForeignKey(PaymentPlans, on_delete=models.SET_NULL, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='pending')
