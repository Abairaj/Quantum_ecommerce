from django.contrib import admin
from.models import *

# Register your models here.



class AdminProduct(admin.ModelAdmin):
    model = Product
    list_display = ('product_name', 'category','brand') 
    
    readonly_fields = ('time_added',)
    ordering = ('time_added', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(Product,AdminProduct)


class Admincolor(admin.ModelAdmin):
    model = Color
    list_display = ('name', 'product') 


    def __str__(self):
        return self.color.product


admin.site.register(Color,Admincolor)




class AdminVariant(admin.ModelAdmin):
    model = Variant

    list_display = ( 'color','price','discount_percentage','quantity') 
    

    def __str__(self):
        return self.product


admin.site.register(Variant,AdminVariant)


admin.site.register(Image)