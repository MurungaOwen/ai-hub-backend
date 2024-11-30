from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from decouple import config
from .models import StripeCustomers, PaymentPlans
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


checkout_session_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'plan_id': openapi.Schema(type=openapi.TYPE_STRING, description="The ID of the plan to subscribe to")
    },
    required=['plan_id']
)

checkout_session_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'url': openapi.Schema(type=openapi.TYPE_STRING, description="The URL for the Stripe Checkout session"),
        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Error message in case of failure")
    }
)

@swagger_auto_schema(
    tags=['Payment'],
    method='post',
    request_body=checkout_session_request_schema,
    responses={201: checkout_session_response_schema, 400: 'Bad Request'}
)
@api_view(['POST'])
def checkout_session_view(request):
    try:
        stripe.api_key = config('STRIPE_SECRET_KEY')
        data = request.data
        plan_id = data.get('plan_id', None)
        
        # Validate the plan exists
        try:
            plan = PaymentPlans.objects.get(id=plan_id)
        except PaymentPlans.DoesNotExist:
            return Response({'error': 'Invalid plan ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check or create Stripe customer
        try:
            customer = StripeCustomers.objects.get(user=request.user)
        except StripeCustomers.DoesNotExist:
            stripe_customer = stripe.Customer.create(email=request.user.email)
            customer = StripeCustomers.objects.create(
                user=request.user, stripe_customer_id=stripe_customer.id, current_plan=plan
            )
        
        # Check if user has an active subscription
        if customer.current_plan and customer.current_plan.status == 'active':
            return Response({'error': 'You already have an active subscription'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create a checkout session
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f"{settings.CLIENT_URL}/checkout/success",
            cancel_url=f"{settings.CLIENT_URL}/checkout/canceled",
            customer=customer.stripe_customer_id,
            customer_update={
                'address': 'auto',  # Let Stripe handle the address
            },
        )
        return Response({'url': session.url}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
