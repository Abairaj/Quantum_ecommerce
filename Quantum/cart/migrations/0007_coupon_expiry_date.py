# Generated by Django 4.1.5 on 2023-01-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_coupon_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
