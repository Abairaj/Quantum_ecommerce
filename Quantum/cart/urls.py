from django.urls import path, include
from .views import *
from .views import *

urlpatterns = [
    path('add_to_cart/<str:id>', AddtocartAPIView.as_view(), name='add_to_cart'),
    path('', CartView.as_view(), name='cart'),
    path('manage_cart/<str:id>/<str:action>', ManageCartView.as_view(), name='manage_cart'),
    # path('checkout/',CheckoutAPIView.as_view(),name = 'checkout'),
    path('add_address/',add_addressform,name = 'add_address'), 
   

]