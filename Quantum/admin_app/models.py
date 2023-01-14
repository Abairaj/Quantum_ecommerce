from django.db import models
from user. models import *
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=300)
    category_image = models.ImageField(upload_to='products/category_image/',null=True,blank=True)
    commission = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=300)
    brand_logo = models.ImageField(upload_to='products/brand_image/',null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name


class Banner(models.Model):
    banner_id = models.IntegerField(default=1)
    banner_title = models.CharField(max_length = 300)
    banner_image = models.ImageField(upload_to='banners/',blank=True,null=True)
    banner_description = models.CharField(max_length=500)
    



