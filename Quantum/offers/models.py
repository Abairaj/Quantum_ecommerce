from django.db import models
from user.models import users
from admin_app.models import Brand

# Create your models here.

class Offer(models.Model):
    offer_name = models.CharField(max_length=50)
    vendor_id = models.ForeignKey(users,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
    percent = models.FloatField()
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    expiry_date = models.DateField(null=True,blank=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.offer_name