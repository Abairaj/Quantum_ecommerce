from django.contrib import admin
from.models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('product_id','id','order_date','user_address','status') 
    
  
    ordering = ('order_date', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(Order,OrderAdmin)



class PaymentAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('user_id', 'amount', 'payment_method','expiry_date','is_active') 
    


    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(Payment,PaymentAdmin)