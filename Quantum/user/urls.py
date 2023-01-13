from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('shop/',views.shop,name='shop'),
    path('signin', views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'),
    path('forgetpassword/',views.forget_password,name='forgetpass'),
    path('product_details/<str:id>/',views.product_detail,name='product_details'),
    path('logout/',views.logout,name='logout'),
    path('otp_login',views.otp_login,name='otp_login'),
    path('verify_login/<str:id>',views.verify_login,name='verify_login'),



]