from django.urls import path
from . import views
urlpatterns = [
    path('signin', views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'),
    path('otp_login',views.otp_login,name='otp_login'),
    path('otp_signup',views.otp_signup,name='otp_signup'),
    path('forgetpassword',views.forget_password,name='forgetpass'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout')



]