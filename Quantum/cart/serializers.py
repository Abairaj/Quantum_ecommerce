from rest_framework import serializers
from.models import *


from rest_framework import serializers

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ( '__all__')

class Add_CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ['id']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_items
        fields = ('__all__')

class Add_CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_items
        fields = ('__all__')