from django.contrib import admin
from user.models import *
# Register your models here.


class usersAdmin(admin.ModelAdmin):
    model = users
    list_display = ('first_name', 'email', 'mobile', 'gender','is_staff','is_verified','is_active','last_login','date_joined') 
    
    readonly_fields = ('last_login','date_joined')
    ordering = ('date_joined', )
    filter_horizontal =()
    list_filter = ()
    fieldsets =()


admin.site.register(users,usersAdmin)
admin.site.register(Address)



admin.site.register(Wallet)