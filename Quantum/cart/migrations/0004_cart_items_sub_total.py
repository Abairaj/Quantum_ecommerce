# Generated by Django 4.1.5 on 2023-01-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_rename_cart_id_cart_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_items',
            name='sub_total',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
    ]