from django.urls import path, include
from .views import *
from .views import *

urlpatterns = [
    path('add_to_cart/<str:id>', AddtocartAPIView.as_view(), name='add_to_cart'),
    path('', CartView.as_view(), name='cart'),
    path('manage_cart/<str:id>/<str:action>', ManageCartView.as_view(), name='manage_cart'),
    path('address/',addressform,name = 'address'),
    path('address_default/<str:id>/<str:action>',address_default,name = 'address_default'),
    path('add_address/',Manage_address_View.as_view(),name = 'add_address'), 
   

]