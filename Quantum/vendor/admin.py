from django.contrib import admin
from.models import *

# Register your models here.



class AdminProduct(admin.ModelAdmin):
    model = Product
    list_display = ('product_name', 'price', 'discount_price', 'category','brand','quantity') 
    
    readonly_fields = ('time_added',)
    ordering = ('time_added', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(Product,AdminProduct)
