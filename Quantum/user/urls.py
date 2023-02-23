from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('user_profile',views.user_profile.as_view(),name = 'user_profile'),
    path('user_profile_management/',views.user_profile_management.as_view(),name = 'user_profile_management'),
    path('user_profile_edit',views.user_profile_edit.as_view(),name = 'user_pro_edit'),
    path('user_add_address',views.User_add_address_view.as_view(),name = 'user_add_address'),
    path('shop/',views.shop,name='shop'),
    path('signin/',views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'),
    path('mobile_verify',views.mobile_verify, name='mobile_verify'),
    path('forgetpassword/',views.forgot_password,name='forgetpass'),
    path('forgot_otp_verify/',views.forgot_password_verify,name='forgot_otp_verify'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('product_details/<str:id>/<str:v_id>',views.product_detail,name='product_details'),
    path('logout/',views.logout,name='logout'),
    path('otp_login',views.otp_login,name='otp_login'),
    path('verify_login/<str:id>',views.verify_login,name='verify_login'),
    path('category_filter/<str:id>',views.Category_filter.as_view(),name = 'category_filter'),
    path('shop_searchbar/',views.search_bar,name = 'shop_searchbar'),
    path('autolist/',views.product_list_ajax,name='autolist'),
    path('wallet/',views.Wallet_view.as_view(),name = 'wallet'),
    path('filter/',views.filter,name = 'filter'),
    path('brand_filter/<str:id>',views.brand_filter,name ='brand_filter')
    
    



]