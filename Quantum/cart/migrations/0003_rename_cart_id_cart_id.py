# Generated by Django 4.1.5 on 2023-01-17 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_id_cart_cart_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cart_id',
            new_name='id',
        ),
    ]
