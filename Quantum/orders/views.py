from urllib import response
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from cart.forms import AddressForm
from cart.models import Cart,Cart_items
from django.views.generic import View,TemplateView,CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import random
import razorpay
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from .models import Address,Payment,razorpay_details
from datetime import datetime
from user.models import users,Wallet
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from user.views import user_check



# Create your views here.


client = razorpay.Client(auth =(settings.KEY , settings.SECRET))
client.set_app_details({"title" : "Django", "version" : "4.1.5"})


def split_payment(amount,admin_percentage,id):
     
     admin_amount = (admin_percentage/100) * amount * 100

     vendor_amount = (amount - admin_amount) * 100

     payment = client.payment.capture(amount,id)

     client.refund.create(payment["id"], {"amount": vendor_amount})

    # refund the admin's share of the payment
     client.refund.create(payment["id"], {"amount": admin_amount})
     return payment



@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
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
        
        # creating razorpay order
        try:
          payment = client.order.create(dict({'amount': cart.total*100,'currency':'INR','payment_capture':1}))
        except:
             messages.warning(self.request,'Please check your internet connection and try again')
             return redirect('cart')
        carts = self.request.session.get('cart_id')
        cart1 = Cart_items.objects.filter(cart = carts).count()
        addressdef = Address.objects.filter(default = True)
        try:
         coupon = self.request.session.get('coupon')
         del self.request.session['coupon']
        except Exception as e:
             print(e)
        context = {'carts':cart1,'cart':cart,'coupon':coupon,'addressdef':addressdef,'payment':payment,'form':self.form_class,'key':settings.KEY}
        return context




@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
class PaymentAPI(View):   
   def post(self,request,**kwargs):
            amt = self.kwargs.get('amount')
            data = request.POST['payment_method']
            user_id = users.objects.get(id = request.user.id)
            if Address.objects.filter(user = request.user.id).filter(default = True).exists():
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
                Variant = i.variant,
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
    
        




@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
class OrderTracking(TemplateView):
     template_name = 'Dashboard.html'

     def get_context_data(self, **kwargs):
          
          context =  super().get_context_data(**kwargs)

          order_id = Order.objects.filter(user_id = self.request.user.id).order_by('-order_date')
          context['order'] = order_id
          carts = self.request.session.get('cart_id')
          cart = Cart_items.objects.filter(cart = carts).count()
          context['cart'] = cart

          return context
     


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
class user_order_view(TemplateView):
     template_name = 'user_order_details.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)

          id = self.kwargs.get('id')
          
          order = Order.objects.filter(id = id)

          context['order'] = order
          carts = self.request.session.get('cart_id')
          cart = Cart_items.objects.filter(cart = carts).count()
          context['cart'] = cart

          return context





# razorpay_payment
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
class success(View):

    def get(self,request, **kwargs):
         rz_signature =self.request.GET.get('signature')
         rz_order_id = self.request.GET.get('order_id')
         rz_payment_id = self.request.GET.get('payment_id')





         params_dict = {
              'razorpay_order_id':rz_order_id,
              'razorpay_payment_id':rz_payment_id,
              'razorpay_signature':rz_signature
         }
         cart = self.request.session['cart_id']
         cart = Cart.objects.get(id = cart)
         user_id = users.objects.get(id = self.request.user.id)
         cart_items = Cart_items.objects.filter(cart = cart)
         total_perc = 0


        #  verifying payment_signature
         result = client.utility.verify_payment_signature(params_dict)
         if result is not None:
            if Address.objects.filter(user_id = self.request.user.id).filter(default = True).exists():
                address =Address.objects.filter(default = True).get(user_id = user_id)
            else:
                messages.warning(self.request,'Set a default address and continue order')
                return redirect('checkout')
            
            for i in cart_items:
                admin_per = i.product.category.commission * i.quantity
                total_perc += admin_per

            for i in cart_items:
                vendor_earnings = i.product.final_price - (i.product.final_price * total_perc / 100)
                wallet, created = Wallet.objects.get_or_create(user_id=i.product.vendor_name)
                wallet.balance += vendor_earnings
                wallet.save()

                    
            
                    
                raz_details = razorpay_details.objects.create(
                    
                razorpay_order_id = self.request.GET.get('razorpay_order_id'),
                razorpay_payment_id =self.request.GET.get('razorpay_payment_id'),
                razorpay_payment_signature =self.request.GET.get('razorpay_signature'),
                )
                    


    

                payment =Payment.objects.create(
                    user_id = user_id,
                    amount = cart.total,
                    payment_method = 'Razorpay',
                    raz_id = raz_details

                )


                    # creating order
                cart_id = self.request.session.get('cart_id')
                cart = Cart.objects.get(id = cart_id)
                cart_items = Cart_items.objects.filter(cart = cart)
                address =Address.objects.filter(default = True).get(user_id = user_id)
                print(address)
                order_ids = []


                for i in cart_items:
                    id = random.randint(100000,999999)
                    order =Order.objects.create(
                    id = id,
                    cart = cart,
                    payment_id = Payment.objects.get(id = payment.id),
                    product_id = i.product,
                    Variant = i.variant,
                    user_id = user_id,
                    user_address = address,
                    amount = i.price * i.quantity,
                    quantity = i.quantity
                            )

                    
                    order_ids.append(int(id))
                    
                    

                    i.delete()
                    cart_items.delete()
                    cart.total = 0
                    cart.save()

             

                return redirect('invoice',order_ids)
         else:
                    messages.warning(self.request,'Payment Failed.Try again')
                    return redirect('checkout')

        








@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
class product_return(View):
     def post(self,request,**kwargs):
       return redirect('orders')
     




@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
class cancel_order(View):
     
     def get(self,request,**kwargs):
         order_id = kwargs["id"]
         user = self.request.user.id
         user_id = users.objects.get(id = user)
         order =  Order.objects.get(id = order_id)
         order.status = 'Cancelled'
         order.save()
         if order.payment_id.payment_method == 'Razorpay':
             
     
                wallet = Wallet.objects.get(user_id = user_id)
                wallet.balance +=  order.amount           
                wallet.save()

                messages.success(request,f'order cancelled and amount of Rs{order.amount} added to wallet.')
                return redirect('order_tracking')
         
         else:
              messages.success(request,'Order is cancelled successfully')
              return redirect('order_tracking')






@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_check, name='dispatch')
class return_order(View):
     
     def get(self,request,**kwargs):
         order_id = kwargs["id"]
         user = self.request.user.id
         user_id = users.objects.get(id = user)
         order =  Order.objects.filter(id__in = order_id)
         order.status = 'Returned'
         order.save()
         if order.payment_id.payment_method == 'Razorpay':
             
     
                wallet = Wallet.objects.get(user_id = user_id)
                wallet.balance +=  order.amount           
                wallet.save()

                messages.success(request,f'order return accepted  and amount of Rs{order.amount} added to wallet after confirming the order return.')
                return redirect('order_tracking')
         else:
              messages.success(request,'Order return accepted we will get the order from you soon.Payment will be refunded soon after return confirmation')
              return redirect('order_tracking')
         
          
         

@csrf_exempt
@login_required(login_url='/')
@user_check
def invoice(request, order_id):
    # print(type(order_ids))
 
 #order_id is in str convert to list
    order_ids = order_id.strip('[]').split(',')
    order_ids = [int(id) for id in order_ids]
    orders = Order.objects.filter(id__in=order_ids)
    date = datetime.today()
    order_total = 0

    for i in orders:
         order_total += i.Variant.final_price
    
    try:
        action = request.GET.get('action')
    except:
         action =None
     
    if request.GET.get('action') == 'download':
        # Create a file-like buffer to receive PDF data.
     # Create the HttpResponse object with the appropriate PDF headers.
       response = HttpResponse(content_type='application/pdf')
       response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    # Create the PDF object, using the response object as its "file."
       doc = SimpleDocTemplate(response,title ='Quantum Times Invoice')

    # Container for the 'Flowable' objects
       elements = []

    # Table header
       data = [["Item", "Variant", "Quantity", "Price"]]

    # Table rows
       for order in orders:
            data.append([order.product_id.product_name, order.Variant.color.name, order.quantity, order.amount])
       data.append(["","" ,"Order Total", order_total])

       
       
       table = Table(data)
       table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (0.75, 0.75, 0.75)),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), (0.93, 0.93, 0.93)),
            ('GRID', (0, 0), (-1, -1), 1, (0.75, 0.75, 0.75,0.75))
        ]))

    # Add table to the PDF
       elements = []
       elements.append(table)
       doc.build(elements)

       

       return response
    
    

         
    return render(request,'invoice.html',{'order':orders,'order_total':order_total,'date':date,'order_id':order_id})








@login_required(login_url='/') 
@user_check
def thanku(request):
    user = request.user
    return render(request,'thanku.html')




























       

