from django.shortcuts import render,redirect
from rest_framework.renderers import TemplateHTMLRenderer
from .forms import AddressForm
from.serializers import *
from.models import *
from vendor.models import*
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View,TemplateView,CreateView
from django.http import HttpResponse
from rest_framework import status
from django.db.models import Q
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


@method_decorator(login_required(login_url='signin'), name='dispatch')
class  AddtocartAPIView (TemplateView):
    template_name = 'cart.html'
    
    def get(self,request, **kwargs):
        
        user = self.request.user
        #get product id
        product_id = self.kwargs['id']
       
      #get product
        product = Product.objects.get(id = product_id)

        #check if cart exists()
        cart_id = self.request.session.get('cart_id')
        print(cart_id)
        if cart_id:
            cart = Cart.objects.get(user_id = self.request.user.id)
            in_cart =Cart_items.objects.filter(product = product)

#  if items already exist in cart increase quantity and subtotal
            if in_cart.exists():
                cart_items = in_cart.last()
                cart_items.quantity += 1
                cart_items.sub_total += product.discount_price
                cart_items.save()
                cart.total += product.discount_price
                cart.save()
# if new item addedd to cart ne cart product will be created
            else:
                cart_item = Cart_items.objects.create(cart = cart, product = product, price = product.discount_price,quantity = 1,sub_total = product.discount_price)
                cart_item.save()
                cart.total += product.discount_price
                cart.save()

        else:
          messages.warning(request,'invalid account')
          return redirect('home')


           
        #check if product already exist in cart
        return redirect("cart")


@method_decorator(login_required(login_url='signin'), name='dispatch')
class CartView(TemplateView):
    template_name = "cart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id = cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

@method_decorator(login_required(login_url='signin'), name='dispatch')
class ManageCartView(View):

    def get(self,request,*args,**kwargs):
        user = self.request.user
        product_id =self.kwargs['id']
        action = self.kwargs.get('action')
        cart_item = Cart_items.objects.get(id = product_id)
        cart = cart_item.cart
        cart.save()
  
   
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.sub_total += cart_item.price
            cart_item.save()
            cart.total += cart_item.price
            cart.save()


        if action == 'decrease':
            if cart_item.quantity == 1:
                cart_item.delete()
                cart.total -= cart_item.price
                cart.save()
                return redirect('cart')
            cart_item.quantity -= 1
            cart_item.sub_total -= cart_item.price
            cart_item.save()
            cart.total -= cart_item.price
            cart.save()
            

        if action == 'delete':
            cart.total -= cart_item.sub_total
            cart.save()
            cart_item.delete()



        return redirect("cart")
        

@method_decorator(login_required(login_url='signin'), name='dispatch')
class Manage_address_View(TemplateView):
    template_name = "addresses.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        address = Address.objects.all()

        context['address'] = address
        return context



@never_cache
@login_required(login_url='signin')
def add_addressform(request):
    
    if request.POST:
        form = AddressForm(request.POST)
        print(form.errors)       
        if form.is_valid():

            form.instance.user = users.objects.get(id = request.user.id)
            form.save()
            return redirect('checkout')
    return render(request,'addresses.html',{'form':AddressForm})

    
@login_required(login_url='signin')
def addressform(request):

    if request.POST:
        form = AddressForm(request.POST)
        print(form.errors) 
        

        if form.is_valid():
            
            form.instance.user = users.objects.get(id = request.user.id)
            form.save()
            return redirect('checkout')
        else:
            messages.warning(request,' Please submit the form with proper values')
            return redirect('checkout')
    return render('checkout',{'form':form})


def address_default(request,id,action):

    address = Address.objects.get(id = id)

    if action == 'default':
        address.default = True
        address.save()

        other = Address.objects.exclude(id = id)
        for i in other:
            i.default = False
            i.save()

        return redirect("add_address")
    else:
        address.delete()
        messages.success(request,'successfully delted the address')
        return redirect('add_address')

    
