from rest_framework import serializers
from .models import *

class Orderserializer(serializers.Serializer):
    class Meta:
        model = Order
        fields = ('__all__')

class Paymentserializer(serializers.Serializer):
    class Meta:
        model = Payment
        fields = ('__all__')
