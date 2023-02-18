# Generated by Django 4.1.5 on 2023-02-18 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_rename_image_1_image_image_remove_image_image_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='variant',
            field=models.ManyToManyField(related_name='images', to='vendor.variant'),
        ),
    ]
