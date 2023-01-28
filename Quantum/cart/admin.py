from django.contrib import admin
from.models import *

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('id','user_id','created_at','updated_at') 
    
    readonly_fields = ()
    ordering = ('created_at', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(Cart,CartAdmin)


class Cart_itemsAdmin(admin.ModelAdmin):
    model = Cart_items
    list_display = ('id','cart','product','quantity','price') 
    


admin.site.register(Cart_items,Cart_itemsAdmin)


admin.site.register(Coupon)