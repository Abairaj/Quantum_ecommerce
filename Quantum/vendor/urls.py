from django.urls import path
from . import views
urlpatterns = [
    path('',views.vendor_dashboard,name = 'vendor_dashboard'),
    path('vendor-signin/', views.vendor_signin, name = 'vendor-signin'),
    path('vendor-signup/',views.vendor_signup,name='vendor-signup'),
    path('vendor-logout/',views.logout,name = 'vendor-logout'),
    path('vendor_products/',views.vendor_products,name = 'vendor_products'),
    path('vendor_orders', views.vendor_orders,name = 'vendor_orders'),
    path('vendor_coupon', views.vendor_coupon,name = 'vendor_coupon'),
    path('vendor_offers', views.vendor_offers,name = 'vendor_offers'),
    path('vendor_salesreport', views.vendor_salesreport,name = 'vendor_salesreport'),

]