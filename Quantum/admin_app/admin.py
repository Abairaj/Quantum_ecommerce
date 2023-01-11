from django.contrib import admin
from .models import*

# Register your models here.
class AdminCategory(admin.ModelAdmin):
    model = Category
    list_display = ('category_name','date_added','last_update') 
    
    readonly_fields = ('date_added','last_update')
    ordering = ('date_added', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(Category,AdminCategory)


class AdminBrand(admin.ModelAdmin):
    model = Brand
    list_display = ('brand_name','date_added','last_update') 
    
    readonly_fields = ('date_added','last_update')
    ordering = ('date_added', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()

admin.site.register(Brand,AdminBrand)


class AdminBanner(admin.ModelAdmin):
    model = Banner
    list_display = ('banner_title','banner_description') 

admin.site.register(Banner,AdminBanner)



