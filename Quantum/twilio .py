# from django import forms
# import django
# from django.contrib.auth.backends import RemoteUserBackend
# from django.db import models
# from django.forms.widgets import PasswordInput
# from django.http.response import HttpResponse
# from django.shortcuts import redirect, render
# from django.contrib import messages, auth
# from cart.models import CartItem
# from cart.views import _cart_id
# from category.models import Category
# from showroom.models import ReviewRating, Variant, Vehicle
# from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string, get_template
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import EmailMessage
# from cart.models import Cart
# from banners.models import Banner
# from showroom.views import review
# from user.forms import RegistrationForm
# from user.models import Account, Address
# from django.contrib.auth.decorators import login_required
# from orders.models import Order
# from send_code import send_code
# from check_code import check_code
# from django.views.decorators.csrf import csrf_exempt



















# @csrf_exempt
# def register(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             email = form.cleaned_data['email']
#             gender = form.cleaned_data['gender']
#             mobile = form.cleaned_data['mobile']
#             password = form.cleaned_data['password']
#             try:
#                 user = Account.objects.create_user(
#                     first_name=first_name, last_name=last_name, email=email, gender=gender, mobile=mobile, password=password)

#                 user.save()

#                 print('User Created')
#                 #messages.success(request,'Registration Successful')

#                 request.session['mobile'] = mobile
#                 return redirect('send-otp')
#             except:
#                 messages.success(request, 'Account already exists..')
#                 return redirect('register')

#         print('form not valid')
#     else:
#         form = RegistrationForm()
#     context = {
#         'form': form,
#     }
#     print('welcome to registration page')
#     return render(request, 'register.html', context)











# def verify_otp(request):
#     if request.method == "POST":
#         entered_code = str(request.POST['first'])+str(request.POST['second'])+str(
#             request.POST['third'])+str(request.POST['fourth'])
#         mobile = request.session['mobile']
#         if check_code(mobile, entered_code):
#             user = Account.objects.get(mobile=mobile)
#             user.is_verified = True
#             user.save()
#             #send_welcome_msg(str(mobile))
#             auth.login(request, user)
#             return redirect('home')
#         else:
            
#             messages.error(request, "OTP not matching...Try Again")
#             return redirect('verify-otp')

#     else:
#         try:
#             mobile = request.session['mobile']
#             print("otp sending...")
#             send_code(mobile)
#         except:
#             print("twilio error....!!")
#             pass

#         return render(request, 'otp_codepen/otp.html', {'mobile': mobile})








# def otp_login(request):
#     if request.method == "POST":

#         try:
#             mobile = request.POST['mobile']
#             user = Account.objects.get(mobile=mobile, is_staff=False)
#         except:
#             user = None
#         if user is not None:
#             try:
#                 request.session['mobile'] = mobile
#                 send_code(mobile)
#                 print("Login otp sent")
#             except:
#                 print("twilio error....!!")
#                 pass
#             return redirect('check-login-otp')
#         else:
#             messages.info(request, "Mobile number is not registered")
#             print("Mobile not registrered")
#             return redirect('otp-login')

#     else:
#         return render(request, 'otp_signin.html')


# def check_login_otp(request):
#     if request.method == "POST":
#         otp = request.POST['otp']
#         try:
#             mobile = request.session['mobile']
#             if check_code(mobile, otp):
#                 user = Account.objects.get(mobile=mobile)
#                 user.is_verified = True
#                 user.save()

#                 auth.login(request, user)
#                 return redirect('home')
#             else:
#                 messages.info(request, "Password not matching..Try Again..!")
#                 return redirect('otp-login')

#         except:
#             messages.info(request, "Somthing Went Wrong")
#             return redirect('otp-login')
#     else:
#          return render(request, 'otp-check.html')


# def view_category_store(request, pk=None):
#     print("------------>>>>>>>>>")
#     # try:
#     vehicles = Vehicle.objects.filter(category=pk,is_available=True)
#     if pk==None:
#         vehicles_count=vehicles.count()
#         categories=Category.objects.all()
#         paginator=Paginator(vehicles,6)
#         page=request.GET.get('page')
#         paged_vehicles=paginator.get_page(page)

#         return render(request, 'store.html', {'vehicles': paged_vehicles,'categories':categories,'vehicles_count':vehicles_count})

#     vehicles_count=vehicles.count()
#     categories=Category.objects.all()
#     category_title=Category.objects.get(id=pk).category_name
#     paginator=Paginator(vehicles,6)
#     page=request.GET.get('page')
#     paged_vehicles=paginator.get_page(page)
#     return render(request, 'store.html', {'vehicles': paged_vehicles,'categories':categories,'category_title':category_title,'vehicles_count':vehicles_count})
#     # except:
#         # return redirect('/')


































#         # send code

#         import os
# from twilio.rest import Client
# from django.conf import settings

# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# def send_code(mobile):

#     account_sid = settings.TWILIO_ACCOUNT_SID
#     auth_token =settings.TWILIO_AUTH_TOKEN
#     client = Client(account_sid, auth_token)

#     verification = client.verify \
#                         .services(settings.VERIFICATION_SID) \
#                         .verifications \
#                         .create(to='+91'+mobile, channel='sms')

#     print(verification.status)









#     # check code

#     import os
# from twilio.rest import Client
# from django.conf import settings

# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# def check_code(mobile,entered_code):

#     account_sid = settings.TWILIO_ACCOUNT_SID
#     auth_token =settings.TWILIO_AUTH_TOKEN
#     client = Client(account_sid, auth_token)

#     verification_check = client.verify \
#                             .services(settings.VERIFICATION_SID) \
#                             .verification_checks \
#                             .create(to='+91'+mobile, code=entered_code)

#     print(verification_check.status)
#     if(verification_check.status=="approved"):
#         print("OTP verified")
#         return True
#     else:
#         return False