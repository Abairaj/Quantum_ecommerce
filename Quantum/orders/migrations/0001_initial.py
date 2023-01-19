# Generated by Django 4.1.5 on 2023-01-17 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0004_remove_product_otp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0006_alter_users_otps'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('payment_type', models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Credit Card Payment', 'Credit Card Payment'), ('Netbanking', 'Netbanking'), ('UPI', 'UPI')], max_length=50)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], max_length=15, null=True)),
                ('quantity', models.IntegerField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.product')),
                ('user_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.address')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('payment_method', models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Razorpay', 'Razorpay')], max_length=20)),
                ('expiry_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]