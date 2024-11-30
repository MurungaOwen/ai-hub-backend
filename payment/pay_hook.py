from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .models import PaymentTransaction, StripeCustomers
import stripe
from datetime import datetime
from decouple import config
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema


stripe.api_key = config('STRIPE_SECRET_KEY')


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = config('STRIPE_ENDPOINT_SECRET')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )

            # Handle specific event types
            if event["type"] == 'customer.subscription.created':
                print("Event Data: ", event)
                self.handle_payment_success(event)

            elif event["type"] == "invoice.payment_failed":
                invoice = event["data"]["object"]
                self.handle_payment_failed(invoice)

            elif event["type"] == "customer.subscription.updated":
                subscription = event["data"]["object"]
                self.handle_subscription_update(subscription)

            elif event["type"] == "customer.subscription.deleted":
                subscription = event["data"]["object"]
                self.handle_subscription_cancellation(subscription)

            return JsonResponse({"success": True})
        except ValueError as e:
            return JsonResponse({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({"error": "Invalid signature"}, status=400)

    def handle_payment_success(self, event):
        stripe_subscription = stripe.Subscription.retrieve(event['data']['object']['id'])
        customer = StripeCustomers.objects.get(stripe_customer_id=stripe_subscription.customer)
        customer.subscription_start=timezone.make_aware(datetime.fromtimestamp(stripe_subscription.created))
        customer.subscription_end = timezone.make_aware(datetime.fromtimestamp(stripe_subscription.current_period_end))
        customer.status='active'
        customer.save()

        user = customer.user
        user.is_premium = True
        user.premium_expiry = timezone.make_aware(datetime.fromtimestamp(stripe_subscription.current_period_end))
        user.save()

        PaymentTransaction.objects.create(
            user=customer.user,
            stripe_transaction_id=event['data']['object']['id'],
            amount=event['data']['object']['items']['data'][0]['plan']['amount'] / 100,  # Convert from cents
            currency=event['data']['object']['currency'],
            payment_plan=customer.current_plan,
            status='success'
        )

    def handle_payment_failed(self, invoice):
        stripe_transaction_id = invoice.get("id")

        transaction = PaymentTransaction.objects.filter(
            stripe_transaction_id=stripe_transaction_id
        ).first()

        if transaction:
            transaction.status = "failed"
            transaction.save()

    def handle_subscription_update(self, subscription):
        print('subscription is: ',)
        stripe_customer_id = subscription.get("customer")
        current_period_end = subscription.get("current_period_end")

        # Find the StripeCustomer in the database
        stripe_customer = StripeCustomers.objects.get(
            stripe_customer_id=stripe_customer_id
        )

        if stripe_customer:
            stripe_customer.subscription_end = datetime.fromtimestamp(current_period_end)
            stripe_customer.status = subscription.get("status")
            stripe_customer.save()

    def handle_subscription_cancellation(self, subscription):
        # Handle subscription cancellations
        stripe_customer_id = subscription.get("customer")

        # Find the StripeCustomer in the database
        stripe_customer = StripeCustomers.objects.get(
            stripe_customer_id=stripe_customer_id
        )

        if stripe_customer:
            stripe_customer.status = "canceled"
            stripe_customer.save()

payment_webhook = StripeWebhookView.as_view()