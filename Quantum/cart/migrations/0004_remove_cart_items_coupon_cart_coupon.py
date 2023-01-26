# Generated by Django 4.1.5 on 2023-01-25 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_cart_items_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_items',
            name='coupon',
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.coupon'),
        ),
    ]