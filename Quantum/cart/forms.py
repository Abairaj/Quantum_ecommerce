from django.forms import ModelForm
from django import forms
from user.models import Address



class AddressForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address_line_1=forms.CharField(max_length=100)
    address_line_2=forms.CharField(max_length=100)
    landmark=forms.CharField(max_length=50)
    city=forms.CharField(max_length=100)
    state=forms.CharField(max_length=50)
    zip_code=forms.CharField(max_length=10)
    country=forms.CharField(max_length=50)
    mobile=forms.CharField(max_length=10)
   
 
    
    class Meta:
        model = Address
        exclude = ['user']





