from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_signin, name = 'admin_signin'),
    path('admin_pannel',views.admin_pannel,name='admin_pannel'),
    path('admin_logout',views.logout,name = 'admin_logout'),
    path('category',views.category_management,name = 'admin_category'),
    path('users',views.user_management,name = 'admin_users'),
    path('vendors',views.vendor_management,name = 'admin_vendors'),
    path('salesreport',views.sales_report,name = 'admin_salesreport'),
    path('banners',views.banner,name = 'admin_banners'),




]