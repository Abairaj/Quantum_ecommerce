from django.db import models
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=300)
    category_image = models.ImageField(upload_to='products/category_image/')
    date_added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)


class Brand(models.Model):
    brand_name = models.CharField(max_length=300)
    brand_logo = models.ImageField(upload_to='products/brand_image/')
    date_added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)

