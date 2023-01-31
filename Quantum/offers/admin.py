from django.contrib import admin
from .models import Offer

# Register your models here.


class OfferAdmin(admin.ModelAdmin):
    model = Offer
    list_display = ('offer_name', 'percent','expiry_date') 
    
    readonly_fields = ('created_at',)
    ordering = ('created_at', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(Offer,OfferAdmin)