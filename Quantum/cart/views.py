from django.shortcuts import render,redirect
from rest_framework.renderers import TemplateHTMLRenderer
from .forms import AddressForm
from.serializers import *
from.models import *
from vendor.models import*
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import CreateView
from django.http import HttpResponse
from rest_framework import status
from django.db.models import Q
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy



class edit_delete_CartItemAPIView(APIView):

    def get_object(self,id):
        try:
            return Cart_items.objects.filter(cart = id)
        except Cart_items.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


    def put(self,request,id,cart_id):
        Cart_item = Cart_items.objects.get(Q(product = id) & Q(cart = cart_id))
        print(request.data)
        serializer = CartItemSerializer(Cart_item,data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,cart_id):
        cart_item = Cart_items.objects.get(Q(product = id) & Q(cart = cart_id))
        cart_item.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    

class Add_CartItemAPIView(APIView):
    def post(self,request):
        print(request.data)
        serializer = CartItemSerializer(data = request.data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)



class CartItemAPIView(APIView):

    def get_object(self,id):
        try:
            return Cart_items.objects.filter(cart = id)
        except Cart_items.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


    def get(self,request,id):
        cart_item = self.get_object(id)
        serializer = CartItemSerializer(cart_item,many = True)
        return Response(serializer.data)

    def delete(self,request,id):
        cart_item = Cart_items.objects.get(cart = id)
        cart_item.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)







# html part
@login_required(login_url='/signin')
def cart(request):
    user_id = request.user.id
    print(user_id)
    cart = Cart.objects.filter(user_id = user_id)
    cart_items = cart[0].id
    response = requests.get(f'http://127.0.0.1:8000/cart/cart-items/{cart_items}')
    data = response.json()
    dat = {'items':data}
    for i in range(len(data)):
        d= dat['items'][i]['product']
        Product_name = Product.objects.filter(id = d)[0].product_name
        dat['items'][i].update({'p_name':Product_name})
    return render(request,'cart.html',{'dat':dat,'grand_total':cart[0].total})


@login_required(login_url='/signin')
def delete_cart(request,product_id):
    user_id = request.user.id
    print(user_id)
    cart_id = Cart.objects.filter(user_id = user_id)[0].id
    print(cart_id)
    product = Product.objects.get(id = product_id)
    cart = Cart.objects.get(user_id = request.user.id)
# if cart item get deleted total and subtotal will be deducted by price of the deleted item
    cart_item = Cart_items.objects.get(product = product_id)
    cart.total -=  cart_item.sub_total
    cart.save() 
    response = requests.delete(f'http://127.0.0.1:8000/cart/edit_cart-items/{product_id}/{cart_id}')
    messages.success(request,'cart item removed successfully')
    return redirect('cart')
# --------------------------------------------------------------------------------------------------------------

@login_required(login_url='/signin')
def add_to_cart(request,id,price):
    
    product = Product.objects.get(id = id)
    cart = Cart.objects.get(user_id = request.user.id)
    cartitem = Cart_items.objects.filter(product = id)
    
# if existing items added to cart again quantity will increase 
    if cartitem.exists():
        cart_product = cartitem.last()
        cart_product.quantity += 1
        cart_product.sub_total += product.discount_price
        cart_product.save()
        cart.total += product.discount_price
        cart.save()
    else:
        cart_id = cart.id
        cart_id = str(cart_id)
        cart.total += product.discount_price
        cart.save()
        data = {'cart':cart_id,'product':id,'quantity': 1 ,'price':price,'sub_total':price} 
        response = requests.post('http://127.0.0.1:8000/cart/add_cart-items/',json = data)

        

        messages.success(request,'Item added to cart')
    return redirect('shop')


@login_required(login_url='/signin')
def manage_cart(request,id,action):

    product = Product.objects.get(id = id)
    cart = Cart.objects.get(user_id = request.user.id)
    cartitem = Cart_items.objects.get(product = id)

# Increasing qiantity using + button
    if action == "increase":
        cartitem.quantity += 1
        cartitem.sub_total += product.discount_price
        cartitem.save()
        cart.total += product.discount_price
        cart.save()
        return redirect('cart')

# Decreasing qiantity using - button
    if action == "decrease":
        if cartitem.quantity == 1:
            cartitem.delete()
            return redirect('cart')
        else:
            cartitem.quantity -= 1
            cartitem.sub_total -= product.discount_price
            cartitem.save()
            cart.total -= product.discount_price
            cart.save()
            return redirect('cart')
    
    return redirect('cart')


    
# Address form
def add_addressform(request):
    

    if request.POST:
        form = AddressForm(request.POST)
        print(form.errors)       
        if form.is_valid():

            form.instance.user = users.objects.get(id = request.user.id)
            form.save()
            return redirect('home')
    return render(request,'contact.html',{'form':AddressForm})

    
# Address form
def addressform(request):
    if request.POST:
        form = AddressForm(request.POST)
        print(form.errors)       
        if form.is_valid():

            form.instance.user = users.objects.get(id = request.user.id)
            form.save()
            return redirect('home')
    return render(request,'checkout.html',{'form':AddressForm})
