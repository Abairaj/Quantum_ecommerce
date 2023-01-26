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
         ('Returned', 'Returned'),
         
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

class razorpay_details(models.Model):  
    razorpay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature = models.CharField(max_length=100,null=True,blank=True)


class Payment(models.Model):
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=20,choices=Payment_method)
    raz_id = models.ForeignKey(razorpay_details,on_delete=models.CASCADE,null=True,blank=True)
    payment_status = models.BooleanField(default = False)
    expiry_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)


class Order(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment,on_delete=models.CASCADE,null = True,blank=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    Variant = models.ForeignKey(Variant,on_delete=models.CASCADE,null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    user_address = models.ForeignKey(Address,on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status_choices,default='Orderpending', null=True,blank=False)
    amount = models.PositiveIntegerField(default=0)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True,null=True)