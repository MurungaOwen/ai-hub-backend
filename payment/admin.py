from django.contrib import admin
from .models import PaymentTransaction, PaymentPlans, StripeCustomers
import stripe
from decouple import config


stripe.api_key = config('STRIPE_SECRET_KEY')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stripe_transaction_id', 'amount', 'currency', 'transaction_date', 'status')
    list_filter = ('status', 'currency', 'transaction_date')
    search_fields = ('stripe_transaction_id', 'user__username')
    ordering = ('-transaction_date',)
    readonly_fields = ('transaction_date',)

@admin.register(PaymentPlans)
class PaymentPlansAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration')
    list_filter = ('duration',)
    search_fields = ('name',)
    ordering = ('price',)
    readonly_fields = ('stripe_price_id', 'stripe_product_id')

    def save_model(self, request, obj, form, change):
        if not obj.stripe_price_id:
            try:
                # Check if product already exists in Stripe (optional, depending on your setup)
                if not obj.stripe_product_id:
                    # Create a new product in Stripe
                    product = stripe.Product.create(
                        name=obj.name,
                        description=f"Subscription plan for {obj.name}",
                    )
                    obj.stripe_product_id = product.id

                # Create a recurring price for the subscription plan
                price = stripe.Price.create(
                    unit_amount=int(obj.price * 100),
                    currency="usd",
                    product=obj.stripe_product_id,
                    recurring={"interval": "month"},
                )
                obj.stripe_price_id = price.id

            except Exception as e:
                raise ValueError(f"Error creating product or price in Stripe: {str(e)}")

        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        if obj.stripe_product_id and obj.stripe_price_id:
            try:
                # Delete the price in Stripe
                stripe.Price.delete(obj.stripe_price_id)
                
                # Delete the product in Stripe
                stripe.Product.delete(obj.stripe_product_id)
            except Exception as e:
                raise ValueError(f"Error deleting product or price in Stripe: {str(e)}")
        super().delete_model(request, obj)

@admin.register(StripeCustomers)
class StripeCustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'stripe_customer_id', 'current_plan', 'subscription_start', 'subscription_end', 'status')
    list_filter = ('status', 'subscription_start', 'subscription_end')
    search_fields = ('stripe_customer_id', 'current_plan__name')
    ordering = ('-subscription_end',)
