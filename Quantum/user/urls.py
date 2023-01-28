from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('user_profile',views.user_profile.as_view(),name = 'user_profile'),
    path('user_profile_management',views.user_profile_management.as_view(),name = 'user_profile_management'),
    path('shop/',views.shop,name='shop'),
    path('signin/',views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'),
    # path('forgetpassword/',views.forget_password,name='forgetpass'),
    path('product_details/<str:id>/<str:v_id>',views.product_detail,name='product_details'),
    path('logout/',views.logout,name='logout'),
    path('otp_login',views.otp_login,name='otp_login'),
    path('verify_login/<str:id>',views.verify_login,name='verify_login'),
    path('category_filter/<str:id>',views.Category_filter.as_view(),name = 'category_filter'),
    path('shop_searchbar/',views.search_bar,name = 'shop_searchbar'),
    path('wallet/',views.Wallet_view.as_view(),name = 'wallet'),
    



]