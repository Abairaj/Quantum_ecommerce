from django.urls import path
from . import views
urlpatterns = [

    # Vendor authentication and dasshboard
    path('',views.vendor_dashboard,name = 'vendor_dashboard'),
    path('vendor_profile',views.Vendor_profile.as_view(),name = 'vendor_profile'),
    path('vendor_profile_edit',views.vendor_profile_edit.as_view(),name = 'vendor_pro_edit'),
    path('Vendor_profile_management',views.Vendor_profile_management.as_view(),name = 'Vendor_profile_management'),
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





# vendor salesreport
   path('vendor_sales_report/',views.Vendor_Salesreport_view.as_view(),name='vendor_sales_report'),
   path('download_salesreport/',views.vendor_Salesreport_download.as_view(),name = 'download_salesreport'),
   path('salesreport_filter/',views.salesreport_filter.as_view(),name = 'salesreport_filter'),



#vendor otp 
    path('vendor_otp_login',views.vendor_otp_login,name='vendor_otp_login'),
    path('vendor_verify_login/<str:id>',views.vendor_verify_login,name='vendor_verify_login')

]