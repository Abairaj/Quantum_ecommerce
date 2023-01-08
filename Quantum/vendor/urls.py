from django.urls import path
from . import views
urlpatterns = [
    path('',views.vendor_dashboard,name = 'vendor_dashboard'),
    path('vendor-signin/', views.vendor_signin, name = 'vendor-signin'),
    path('vendor-signup/',views.vendor_signup,name='vendor-signup')

]