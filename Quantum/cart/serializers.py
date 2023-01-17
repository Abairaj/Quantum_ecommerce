from rest_framework import serializers
from.models import *


from rest_framework import serializers




class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_items
        fields = ('__all__')
