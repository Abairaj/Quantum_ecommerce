from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth import login
from .models import *
from admin_app.models import *
from vendor. models import *
from django.contrib import messages
from django.core.validators import validate_email
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required
import random
from sendotp import *
# from verifyotp import verify_otp



            



# Create your views here.
@never_cache
def home(request):
    context = {'banner':Banner.objects.all,'product':Product.objects.all()}

    return render(request,'index.html',context)


def shop(request):
    context = {'category':Category.objects.all(),'product':Product.objects.all()[:10]}
    return render(request,'shop.html',context)



def product_detail(request,id):
      
    context ={'product':Product.objects.filter(id=id)}

    print(context)

    return render(request,'product-detail.html',context)



@never_cache
def signin(request):

    if request.user.is_authenticated:
        messages.success(request,'You have already signed in. ')
        return redirect('home')


    elif request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        


        user = auth.authenticate(email = email,password = password)
        
        if user is not None and user.is_active == True:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.warning(request,'Credentials invalid try again.')
            return redirect('signin')
    else:
        return render(request,'login.html')


@never_cache
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        phone_number = request.POST['phone']
        password1 = request.POST['pass-1']
        password2 = request.POST['pass-2']

        if first_name != first_name.capitalize():
            messages.warning(request,'First name should start with capital letter.')
            return redirect('signup')

        elif users.objects.filter(email = email).exists():
            messages.warning(request,'Email is already taken')
            return redirect('signup')
            
        elif email:
                try:
                    validate_email(email)
                except:
                    messages.warning(request,'Enter valid email address.')
                    return redirect('signup')


        if users.objects.filter(mobile = phone_number):
             messages.warning(request,'The phone number is already registered')
             return redirect('signup')
             
        elif len(phone_number) < 10:
            messages.warning(request,'Enter valid mobile number')
            return redirect('signup')
        elif len(password1) < 4:
            messages,Warning(request,'password should be of 4 or more characters')
            return redirect('signup')
        
        elif password1 != password2:
            messages(request,'Password doesnt match with each other')
            return redirect('signup')
        
        else:
        
          user = users.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            mobile = phone_number,
            password = password2,

        )

          user.save()
          messages.success(request,'Registered successfully. Login with your credentials')
          return redirect('signin')
        
    return render(request,'signup.html')








def otp_login(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        user = users.objects.filter(mobile = mobile)
        if not user.exists():
            return redirect('signup')
        
        print(user[0],'-----------------------------')
        print(user[0].otps,'##########################')
        otp_r = str(random.randint(1000,9999))
        print(otp_r,'..................................')
        # user[0].otps = otp_r
        user.update(otps = otp_r)

        print(user[0].otps,'******************')
        user[0].save() 
        id = user[0].id
        # send_otp(mobile,user[0].otps)
        return redirect('verify_login',id)
        
            
    return render(request,'otp_login.html')







def verify_login(request,id):
    type(id)
    print(id,'8888888888888888888888888888888888')

    
    if request.method == 'POST':
        otp = request.POST['otp']
        user = users.objects.get(id = id)
        if otp == user.otps:
            login(request,user)
            return redirect('home')
        else:
          return redirect('signup')
    return render(request,'otp.html',{'id':id})






def forget_password(request):
    return render(request,'forgotpass.html')

@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('home')