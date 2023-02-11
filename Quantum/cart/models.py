from django.db import models
from vendor.models import Product,Variant
from user.models import users
import uuid

# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    expired = models.BooleanField(default=False)
    discount_price = models.FloatField(default=100)
    minimum_amount = models.FloatField(default=500)
    expiry_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.coupon_code

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(users,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    total = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)




class Cart_items(models.Model):
    cart =models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=0)
    price = models.PositiveIntegerField()
    sub_total = models.PositiveIntegerField()





class Wishlist(models.Model):
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)



