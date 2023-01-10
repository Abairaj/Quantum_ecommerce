from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_signin, name = 'admin_signin'),
    path('admin_pannel/',views.admin_pannel,name='admin_pannel'),
    path('admin_logout/',views.logout,name = 'admin_logout'),
    path('category/',views.category_management,name = 'admin_category'),
    path('salesreport/',views.sales_report,name = 'admin_salesreport'),
    path('banners/',views.banner,name = 'admin_banners'),
    path('users/',views.user_management,name = 'admin_users'),
    path('user_delete/<str:id>',views.user_delete, name = 'user_delete'),
    path('vendors/',views.vendor_management,name = 'admin_vendors'),
    path('vendor_delete/<str:id>',views.vendor_delete,name = 'vendor_delete'),
    path('block/<str:id>',views.block,name = 'vendor_block'),
    path('unblock/<str:id>',views.unblock,name = 'vendor_unblock'),

    path('add_category/',views.add_category,name='add_category')





]