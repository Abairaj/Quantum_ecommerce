from django.db import models
from vendor.models import Product
from user.models import users
import uuid

# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    user_id = models.ForeignKey(users,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    total = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class Cart_items(models.Model):
    cart =models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    sub_total = models.PositiveIntegerField()