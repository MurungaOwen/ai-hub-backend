# Generated by Django 5.1.3 on 2024-11-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_paymentplans_stripe_product_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentplans',
            name='stripe_price_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='paymentplans',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]