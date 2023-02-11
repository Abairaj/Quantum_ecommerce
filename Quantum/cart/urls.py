from django.urls import path, include
from .views import *
from .views import *

urlpatterns = [
    path('add_to_cart/<str:id>', AddtocartAPIView.as_view(), name='add_to_cart'),
    path('', CartView.as_view(), name='cart'),
    path('address/',addressform,name = 'address'),
    path('address_default/<str:id>/<str:action>',address_default,name = 'address_default'),
    path('add_address/',Manage_address_View.as_view(),name = 'add_address'), 
    path('apply_coupon/',Coupon_apply.as_view(),name='apply_coupon'),
    path('update_cart_add',update_cart_add,name = 'update_cart_add'),
    path('update_cart_subtract',update_cart_subtract,name = 'update_cart_subtract'),
    path('delete_cart_item/<str:id>',delete_cart_item,name = 'delete_cart_item'),
    path('add_to_wishlist/<str:id>',add_to_wishlist,name = 'add_to_wishlist'),
    path('wishlist_view/',wishlist_view.as_view(),name = 'wishlist_view'),
    path('delete_wishlist_item/<str:id>',delete_wishlist_item,name = 'delete_wishlist_item')

   
   
   

]