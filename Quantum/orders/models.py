from django.db import models
from vendor.models import *
from user.models import *
from cart.models import Cart


# Create your models here.
Status_choices = (

        ('OrderPending', 'Orderpending'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
         
    )

Payment_type = (
    ('Cash on Delivery','Cash on Delivery'),
    ('Credit Card','Credit Card'),
    ('Netbanking','Netbanking'),
    ('UPI','UPI'),
)

Payment_method = (
    ('Cash on Delivery','Cash on Delivery'),
    ('Razorpay','Razorpay'),
)

    


class Payment(models.Model):
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=20,choices=Payment_method)
    expiry_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    user_address = models.ForeignKey(Address,on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status_choices,default='Orderpending', null=True,blank=False)
    amount = models.PositiveIntegerField(default=0)
    quantity = models.IntegerField()