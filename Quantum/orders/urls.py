
from django.urls import path,include
from.views import *


urlpatterns = [

    path('checkout/',CheckoutAPIView.as_view(),name = 'checkout'),
    path('payment/<str:amount>',PaymentAPI.as_view(),name='payment'),
    path('thanku/',thanku,name='thanku'),
    path('user_dashboard/',User_dahboardView.as_view(),name = 'user_dashboard'),


 ]