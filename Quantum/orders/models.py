from django.db import models
from vendor.models import *
from user.models import *

# Create your models here.
Status_choices = (
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

Payment_type = (
    ('Cash on Delivery','Cash on Delivery'),
    ('Credit Card Payment','Credit Card Payment'),
    ('Netbanking','Netbanking'),
    ('UPI','UPI'),
)

Payment_method = (
    ('Cash on Delivery','Cash on Delivery'),
    ('Razorpay','Razorpay'),
)

    
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50,choices=Payment_type)
    order_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    user_address = models.ForeignKey(Address,on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status_choices, null=True,blank=False)
    quantity = models.IntegerField()

class Payment(models.Model):
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=20,choices=Payment_method)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)