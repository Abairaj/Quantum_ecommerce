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
# Create your views here.







@method_decorator(login_required(login_url='signin'), name='dispatch')
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
        context['cart'] = cart
        return context
    
@method_decorator(login_required(login_url='signin'), name='dispatch')
class PaymentAPI(View):   
    def post(self,request,**kwargs):
        amt = self.kwargs.get('amount')
        data = request.POST['payment_method']
        user_id = users.objects.get(id = request.user.id)
        address =Address.objects.filter(default = True).get(user_id = user_id)

        if address:
                Payment.objects.create(
                    user_id = user_id,
                    amount = amt,
                    payment_method = data
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
            cart = cart,
            product_id = i.product,
            user_id = user_id,
            user_address = address,
            amount = i.price * i.quantity,
            quantity = i.quantity
                    )
            i.delete()
            cart.total = 0
            cart.save()

        return redirect('thanku')
    
        


class User_dahboardView(TemplateView):
     template_name = 'Dashboard.html'

     def get_context_data(self, **kwargs):
          context =  super().get_context_data(**kwargs)

          order_id = Order.objects.filter(user_id = self.request.user.id)
          context['order'] = order_id

          return context
     

    
   
def thanku(request):
    return render(request,'thanku.html')
























       

