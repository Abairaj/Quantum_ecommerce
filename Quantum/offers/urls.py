from django.urls import path
from . import views
urlpatterns = [

path('',views.vendor_offers.as_view(),name = 'vendor_offers'),
path('manage_offer/',views.manage_offer.as_view(),name = 'manage_offer'),
path('offer_status/',views.Changeoffer_status.as_view(),name = 'offer_status'),

]