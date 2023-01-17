from django.urls import path, include
from .views import *
from .views import *

urlpatterns = [
    path('cart-items/<str:id>', CartItemAPIView.as_view(), name='cart-items'),
    path('edit_cart-items/<str:id>/<str:cart_id>', edit_delete_CartItemAPIView.as_view(), name='edit_cart-items'),
    path('add_cart-items/', Add_CartItemAPIView.as_view(), name='add_cart-items'),
    



    # html

    path('',cart,name='cart'),
    path('delete_cart_item/<str:product_id>',delete_cart,name = 'del_cart'),
    path('add_to_cart/<str:id>/<str:price>',add_to_cart,name = 'add_to_cart')

]