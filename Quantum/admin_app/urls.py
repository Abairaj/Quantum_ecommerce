from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_signin, name = 'admin_signin'),
    path('admin_pannel/',views.admin_pannel,name='admin_pannel'),
    path('admin_logout/',views.logout,name = 'admin_logout'),
    path('salesreport/',views.sales_report,name = 'admin_salesreport'),
 


    #vendor and user management
    path('users/',views.user_management,name = 'admin_users'),
    path('user_delete/<str:id>',views.user_delete, name = 'user_delete'),
    path('vendors/',views.vendor_management,name = 'admin_vendors'),
    path('vendor_delete/<str:id>',views.vendor_delete,name = 'vendor_delete'),
    #block unblock both for vendor and user
    path('block/<str:id>',views.block,name = 'vendor_block'),
    path('unblock/<str:id>',views.unblock,name = 'vendor_unblock'),
    
    
     # both brand and category are in same 
    path('category/',views.category_management,name = 'admin_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/<str:id>',views.edit_category,name = 'edit_category'),
    path('add_brand/',views.add_brand,name='add_brand'),
    path('delete_category/<str:id>',views.delete_category,name = 'delete_category'),
    path('edit_brand/<str:id>',views.edit_brand,name = 'edit_brand'),
    path('delete_brand/<str:id>',views.delete_brand,name = 'delete_brand'),

    #  Banner management
    path('banners/',views.banner,name = 'admin_banners'),
    path('add_banner/',views.add_banner,name = 'add_banner'),
    path('edit_banner/<str:id>',views.edit_banner,name = 'edit_banner'),
    path('delete_banner/<str:id>',views.delete_banner,name = 'delete_banner'),
    





]