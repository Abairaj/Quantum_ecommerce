# Generated by Django 4.1.5 on 2023-01-24 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='final_price',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]
