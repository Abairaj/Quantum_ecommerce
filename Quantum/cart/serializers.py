from rest_framework import serializers
from.models import *
from user.models import Address


from rest_framework import serializers




class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_items
        fields = ('__all__')



class Formserializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    address_line_1= serializers.CharField(max_length=100)
    address_line_2= serializers.CharField(max_length=100)
    landmark= serializers.CharField(max_length=50)
    city= serializers.CharField(max_length=100)
    state= serializers.CharField(max_length=50)
    zip_code= serializers.CharField(max_length=10)
    country= serializers.CharField(max_length=50)
    mobile= serializers.CharField(max_length=10)


class AddressAPIserializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('__all__')
