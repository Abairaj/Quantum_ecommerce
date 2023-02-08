from django.shortcuts import render,redirect
from .forms import AddressForm
from.serializers import *
from.models import *
from cart.models import Coupon
from vendor.models import*
from django.views.generic import View,TemplateView
from rest_framework import status
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from offers.models import Offer


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
class  AddtocartAPIView (TemplateView):
    template_name = 'cart.html'
    
    
    def get(self,request, **kwargs):
        
        user = self.request.user
        #get product id
        variant_id = self.kwargs['id']
       
      #get product
        product = Variant.objects.get(id = variant_id)
        product_id = Product.objects.get(id = product.Product.pk)

        #check if cart exists()
        cart_id = self.request.session.get('cart_id')
        print(cart_id)
        if cart_id:
            cart = Cart.objects.get(user_id = self.request.user.id)
            in_cart =Cart_items.objects.filter(variant = product.pk)
            variant = Variant.objects.get(id =product.pk)

#  if items already exist in cart increase quantity and subtotal
            if in_cart.exists():
                cart_items = in_cart.last()
                if cart_items.quantity == variant.quantity:
                    messages.warning(request,"The item is currently out of stock")
                    return redirect('cart')
                cart_items.quantity += 1
                cart_items.sub_total += variant.final_price
                cart_items.save()
                cart.total += variant.final_price
                cart.save()

# if new item addedd to cart ne cart product will be created
            else:
                cart_item = Cart_items.objects.create(cart = cart,product =product_id, variant = variant , price = variant.final_price,quantity = 1,sub_total = variant.final_price)
                cart_item.save()
                cart.total += variant.final_price
                cart.save()
             


        else:
          messages.warning(request,'invalid account')
          return redirect('home')


           
        #check if product already exist in cart
        return redirect("cart")



@method_decorator(never_cache, name='dispatch')
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


@never_cache
@login_required(login_url='signin')
def update_cart_add(request):
    if request.method == 'POST':

        cart_item_id  =int(request.POST['product_id'])

        print(cart_item_id)
       

        
        cart = Cart.objects.get(user_id = request.user)
        print(cart)
        print(Cart_items.objects.filter(id = cart_item_id,cart = cart))
        
        if (Cart_items.objects.filter(cart = cart,id = cart_item_id)):
            prod_qty = int(request.POST['product_qty'])
            
            cart_item = Cart_items.objects.get(id = cart_item_id,cart =cart)
            print(cart_item.price)
            print(cart_item.quantity)
            if cart_item.quantity <= 9:
                cart_item.quantity = prod_qty
                cart_item.sub_total = cart_item.price * cart_item.quantity
                cart_item.save()
                cart_item.cart.total += cart_item.price
                cart_item.cart.save()
                return JsonResponse({'status': 'updated successfully'})
        return redirect('home')


@never_cache   
@login_required(login_url='signin')
def update_cart_subtract(request):
    if request.method == 'POST':
        cart_item_id  =int(request.POST['product_id'])

        print(cart_item_id)
       

        cart = Cart.objects.get(user_id = request.user)
        print(cart)
        print(Cart_items.objects.filter(id = cart_item_id,cart = cart))
        
        if (Cart_items.objects.filter(cart = cart,id = cart_item_id)):
            prod_qty = int(request.POST['product_qty'])
            cart_item = Cart_items.objects.get(id = cart_item_id,cart =cart)
            if cart_item.quantity >= 2:
                cart_item.quantity = prod_qty
                cart_item.sub_total = cart_item.price*cart_item.quantity
                cart_item.save()
                cart_item.cart.total -= cart_item.price
                cart_item.cart.save()
                return JsonResponse({'status': 'updated successfully'})
        return redirect('home')


@never_cache
@login_required(login_url='signin')
def delete_cart_item(request,id):
    cart_item = Cart_items.objects.get(id = id)
    cart = Cart.objects.get(user_id = request.user.id)
    cart_item.delete()
    cart.total -= cart_item.price * cart_item.quantity
    cart.save()

    messages.success(request,'Successfully removed the cart item')
    return redirect('cart')

        

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
class Manage_address_View(TemplateView):
    template_name = "addresses.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        address = Address.objects.filter(user_id = self.request.user.id)

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


@never_cache  
@login_required(login_url='signin')
def addressform(request):

    if request.POST:
        form = AddressForm(request.POST)
        print(form.errors) 
        

        if form.is_valid():
            
            form.instance.user = users.objects.get(id = request.user.id)
            form.save()
            if request.GET.get('action') == 'checkout':
              messages.success(request,'Address added successfully')
              return redirect('checkout')
            else:
                messages.success(request,'Address added successfully')
                return redirect('user_profile')
        else:
            messages.warning(request,' Please submit the form with proper values')
            return redirect('checkout')
    return render('checkout',{'form':form})


@never_cache
@login_required(login_url='signin')
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







@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
class Coupon_apply(View):

    def post(self,request,**kwargs):
        coupon_code =request.POST['coupon']
        coupon = Coupon.objects.filter(coupon_code__icontains =  coupon_code)
        cart_id = self.request.session.get('cart_id')
        cart = Cart.objects.get(id = cart_id)

        if coupon:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            if coupon == cart.coupon:
                messages.warning(request,'coupon already used')
                return redirect('checkout')
            if cart.total < coupon.minimum_amount:
                messages.warning(request,f'Coupon is only applicable for purchase over Rs.{coupon.minimun_amount} or more')
                return redirect('checkout')
            if coupon.expired == True:
                messages.warning(request,'Coupon Expired')
                return redirect('checkout')
            
            cart.coupon = Coupon.objects.get(id = coupon.pk)
            cart.total -= coupon.discount_price
            cart.save()
            coupon.expired = True
            coupon.save()
            return redirect('checkout')
        else:
            messages.warning(request,'Coupon Invalid')
            return redirect('checkout')


        

