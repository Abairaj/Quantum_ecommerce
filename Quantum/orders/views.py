from django.shortcuts import render,redirect
from.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from cart.forms import AddressForm
from cart.serializers import CartItemSerializer
from cart.models import Cart,Cart_items
from django.views.generic import View,TemplateView,CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import hmac
import random
import razorpay
from django.conf import settings
# Create your views here.


client = razorpay.Client(auth =(settings.KEY , settings.SECRET))

def split_payment(amount,admin_percentage,id):
     
     admin_amount = (admin_percentage/100) * amount * 100

     vendor_amount = (amount - admin_amount) * 100

     payment = client.payment.capture(amount,id)

     client.refund.create(payment["id"], {"amount": vendor_amount})

    # refund the admin's share of the payment
     client.refund.create(payment["id"], {"amount": admin_amount})
     return payment



class CheckoutAPIView(TemplateView):
    template_name = 'checkout.html'
    form_class = AddressForm
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs) and {'form':self.form_class}
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id = cart_id)

        else:
            cart = None
        
        payment = client.order.create({'amount': cart.total*100,'currency':'INR','payment_capture':1})
        cart.razorpay_order_id = payment['id']
        cart.save()
        context['payment'] = payment
        print(payment)
        context['cart'] = cart
        return context
    
@method_decorator(login_required(login_url='signin'), name='dispatch')
class PaymentAPI(View):   
    def post(self,request,**kwargs):
        amt = self.kwargs.get('amount')
        data = request.POST['payment_method']
        user_id = users.objects.get(id = request.user.id)
        if Address.objects.exists():
            address =Address.objects.filter(default = True).get(user_id = user_id)
        else:
             messages.warning(request,'Set a default address and continue order')
             return redirect('checkout')

        if address:
                payment =Payment.objects.create(
                    user_id = user_id,
                    amount = amt,
                    payment_method = data,
                )
        else:
             messages.warning(request,'Add a default address and try again')
             return redirect('checkout')

        # creating order
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id = cart_id)
        cart_items = Cart_items.objects.filter(cart = cart)
        address =Address.objects.filter(default = True).get(user_id = user_id)
        print(address)


        for i in cart_items:
            Order.objects.create(
            id = random.randint(100000,999999),
            cart = cart,
            payment_id = Payment.objects.get(id = payment.id),
            product_id = i.product,
            user_id = user_id,
            user_address = address,
            amount = i.price * i.quantity,
            quantity = i.quantity
                    )

            i.delete()
            cart_items.delete()
            cart.total = 0
            cart.save()

        return redirect('thanku')
    
        

@method_decorator(login_required(login_url='signin'), name='dispatch')
class OrderTracking(TemplateView):
     template_name = 'Dashboard.html'

     def get_context_data(self, **kwargs):
          
          context =  super().get_context_data(**kwargs)

          order_id = Order.objects.filter(user_id = self.request.user.id)
          context['order'] = order_id

          return context
     

class success(View):

    def get(self,request, **kwargs):
         cart = self.request.session['cart_id']
         cart = Cart.objects.get(id = cart)
         user_id = users.objects.get(id = self.request.user.id)
         cart_items = Cart_items.objects.filter(cart = cart)
         total_perc = 0 
         for i in cart_items:
                admin_per = i.product.category.commission * i.quantity
                total_perc += admin_per
         print(total_perc,'************************************************************')
         if Address.objects.exists():
                address =Address.objects.filter(default = True).get(user_id = user_id)
         else:
             messages.warning(self.request,'Set a default address and continue order')
             return redirect('checkout')

         if address:
                
                raz_details = razorpay_details.objects.create(
                     
                razorpay_order_id = self.request.GET.get('razorpay_order_id'),
                razorpay_payment_id =self.request.GET.get('razorpay_payment_id'),
                razorpay_payment_signature =self.request.GET.get('razorpay_signature'),
                )
                



                # generated_signature = hmac.new(raz_details.razorpay_order_id + "|" + raz_details.razorpay_payment_id, secret);

                # if not (generated_signature == raz_details.razorpay_payment_signature):
                #         messages.warning(request,'Payment is not successfull try again')
                #         return redirect('checkout')
  

                payment =Payment.objects.create(
                    user_id = user_id,
                    amount = cart.total,
                    payment_method = 'Razorpay',
                    raz_id = raz_details

                )
         else:
             messages.warning(self.request,'Add a default address and try again')
             return redirect('checkout')

        # creating order
         cart_id = self.request.session.get('cart_id')
         cart = Cart.objects.get(id = cart_id)
         cart_items = Cart_items.objects.filter(cart = cart)
         address =Address.objects.filter(default = True).get(user_id = user_id)
         print(address)


         for i in cart_items:
            order =Order.objects.create(
            id = random.randint(100000,999999),
            cart = cart,
            payment_id = Payment.objects.get(id = payment.id),
            product_id = i.product,
            user_id = user_id,
            user_address = address,
            amount = i.price * i.quantity,
            quantity = i.quantity
                    )

            i.delete()
            cart_items.delete()
            cart.total = 0
            cart.save()

            return redirect('thanku')



   
def thanku(request):
    user = request.user
    return render(request,'thanku.html')




























       

