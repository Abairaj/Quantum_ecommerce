from django.db import models
from user. models import users
from admin_app.models import *


# Create your models here.



Variant_choice = (
      ('color','color'),
       ('size','size')
)

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    vendor_name = models.ForeignKey(users,on_delete=models.CASCADE,null=True)
    product_image = models.ImageField(upload_to='products/',blank=True,null=True)
    product_description = models.TextField()
    max_price = models.FloatField(null=True,blank=True)
    max_discount = models.FloatField(null = True,blank=True)
    final_price = models.FloatField(null=True,blank = True)
    Variant = models.CharField(max_length=200,choices=Variant_choice,default = 'color',null=True,blank=True)
    time_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product_name
    


class Color(models.Model):
        product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
        name = models.CharField(max_length=20,null=True,blank=True)



        def __str__(self):
              return self.name




class Image(models.Model):
      id = models.BigAutoField(primary_key=True,blank=True)
      product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
      image_1 = models.ImageField(upload_to='variants/',blank=True,null=True)
      image_2 = models.ImageField(upload_to='variants/',blank=True,null=True)
      image_3 = models.ImageField(upload_to='variants/',blank=True,null=True)


      def __str__(self):
            return str(self.pk)
      
     
    



class Variant(models.Model):
        Product = models.ForeignKey(Product,on_delete=models.CASCADE)
        color = models.ForeignKey(Color,on_delete=models.CASCADE)
        price = models.FloatField()
        image = models.ForeignKey(Image,on_delete=models.CASCADE,null=True,blank=True)
        discount_percentage = models.FloatField()
        final_price = models.FloatField()
        quantity = models.IntegerField()
        created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)



        def __str__(self):
              return str(self.pk)


