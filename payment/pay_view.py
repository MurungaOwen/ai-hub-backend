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
        plan = PaymentPlans.objects.get(id=plan_id)
        # check if user already has a customer assosciated, otherwise create it
	    if not StripeCustomers.objects.get(email=request.user.email):
            stripe_customer = stripe.Customer.create(email=request.user.email)
            customer = StripeCustomers.objects.create(
                user=request.user, stripe_customer_id=stripe_customer.id,
                current_plan=plan
            )
            customer.save()

        current_subscription = request.user.customer

        # our app does not support multiple subscriptions per user

        if current_subscription and current_subscription.status == 'active':
            return Response({'error': 'You already have an active subscription'},
                            status=status.HTTP_400_BAD_REQUEST)

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=settings.CLIENT_URL + '/checkout/success',
            cancel_url=settings.CLIENT_URL + '/checkout/canceled',
            #automatic_tax={'enabled': True}, since we havent setup tax yet
            customer=request.user.customer.stripe_customer_id,
            customer_update={
                'address': 'auto' # let stripe handle the address
            }
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'url': session.url}, status=status.HTTP_201_CREATED)
