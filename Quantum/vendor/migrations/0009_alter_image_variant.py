# Generated by Django 4.1.5 on 2023-02-18 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_remove_image_variant_image_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='variant',
            field=models.ManyToManyField(blank=True, related_name='images', to='vendor.variant'),
        ),
    ]