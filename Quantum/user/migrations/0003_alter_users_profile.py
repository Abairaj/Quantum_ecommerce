# Generated by Django 4.1.5 on 2023-01-28 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=models.ImageField(blank=True, upload_to='uploads/profile/'),
        ),
    ]