# Generated by Django 4.1.5 on 2023-01-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='otp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
