
from django.urls import path,include
from.views import *


urlpatterns = [

    path('checkout/',CheckoutAPIView.as_view(),name = 'checkout'),
    path('payment/<str:amount>',PaymentAPI.as_view(),name='payment'),
    path('thanku/',thanku,name='thanku'),
    path('invoice/<str:order>',download_invoice,name = 'invoice'),
    path('order_tracking/',OrderTracking.as_view(),name = 'order_tracking'),
    path('success/',success.as_view(),name = 'success'),
    path('product_return/<str:id>',product_return.as_view(),name = 'product_return'),
    path('cancel_order/<str:id>',cancel_order.as_view(),name = 'cancel_order'),
    path('return_order/<str:id>',return_order.as_view(),name = 'return_order'),
                                                 


 ]