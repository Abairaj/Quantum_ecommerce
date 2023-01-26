from django.urls import path
from . import views
urlpatterns = [

    # Vendor authentication and dasshboard
    path('',views.vendor_dashboard,name = 'vendor_dashboard'),
    path('vendor-signin/', views.vendor_signin, name = 'vendor-signin'),
    path('vendor-signup/',views.vendor_signup,name='vendor-signup'),
    path('vendor-logout/',views.logout,name = 'vendor-logout'),
         

# Vendor product management
    path('vendor_products/',views.vendor_products,name = 'vendor_products'),
    path('add_product',views.add_product,name='add_product'),
    path('delete_product/<str:id>/',views.delete_product,name='delete_product'),
    path('edit_product/<str:id>',views.edit_product,name='edit_product'),
         
# variant management
    path('variant_view/',views.variant_view,name = 'variant_view'),   
    path('vendor_variant/<str:id>',views.variant,name = 'vendor_variant'),
    path('add_variant/<str:id>',views.add_variants,name = 'add_variant'),
    path('edit_variant/<str:id>',views.edit_variant,name = 'edit_variant'),
    path('delete_variant/<str:id>',views.delete_variants,name = 'delete_variant'),
    

#vendor order management    
    path('vendor_orders/', views.Order_management.as_view(),name = 'vendor_orders'),
    path('update_orders/<int:id>', views.Update_order_status.as_view(),name = 'update_orders'),
                                                                     
#vendor coupon management
    path('vendor_coupon/', views.vendor_coupon,name = 'vendor_coupon'),
    path('add_coupon/', views.add_coupon.as_view(),name = 'add_coupon'),
    path('delete_coupon/<str:id>',views.delete_coupon,name = 'delete_coupon'),
    path('edit_coupon/<str:id>',views.edit_coupon,name = 'edit_coupon'),
         
    path('vendor_offers/', views.vendor_offers,name = 'vendor_offers'),
    path('vendor_salesreport/', views.vendor_salesreport,name = 'vendor_salesreport'),

#vendor otp 
    path('vendor_otp_login',views.vendor_otp_login,name='vendor_otp_login'),
    path('vendor_verify_login/<str:id>',views.vendor_verify_login,name='vendor_verify_login')

]