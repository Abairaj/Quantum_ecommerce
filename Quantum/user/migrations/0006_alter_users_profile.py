# Generated by Django 4.1.5 on 2023-02-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_users_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='user_profile/'),
        ),
    ]
