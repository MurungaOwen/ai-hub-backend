from django.urls import path
from .views import list_payment_plans
from .pay_hook import payment_webhook
from .pay_view import checkout_session_view


urlpatterns = [
    path('checkout/', checkout_session_view),
    path('plans/', list_payment_plans),
    path('webhook/', payment_webhook)
]
