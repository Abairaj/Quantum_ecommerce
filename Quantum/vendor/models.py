from django.db import models
from user. models import *
from admin_app.models import *


# Create your models here.

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    vendor_name = models.ForeignKey(users,on_delete=models.CASCADE,null=True)
    product_description = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField()
    discount_price = models.FloatField()
    image_1 = models.ImageField(upload_to='products/',blank=True,null=True)
    image_2 = models.ImageField(upload_to='products/',blank=True,null=True)
    image_3 = models.ImageField(upload_to='products/',blank=True,null=True)
    time_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product_name
    
