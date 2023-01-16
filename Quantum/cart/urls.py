from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
#     path('carts/<int:id>', CartViewSet.as_view({'get': 'list'}), name='carts'),
    path('cart-items/<str:id>/', CartItemViewSet.as_view({'get': 'list'}), name='cart-items'),
    path('add_cart/', Add_CartViewSet.as_view({'post': 'create'}), name='add_cart'),
    path('add_cart_item/', Add_CartItemViewSet.as_view({'post': 'create'}), name='add_cart_item'),
    path('trial/',views.trial,name='trial'),
# ]
    

    path('cart/<int:id>', CartViewSet.as_view({'get': 'list', 'html_view': 'html_view'}), name='my_model'),
]