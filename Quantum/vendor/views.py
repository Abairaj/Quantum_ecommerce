from django.shortcuts import render,redirect
from django.contrib import messages
from user.models import users
from django.core.validators import validate_email


# Create your views here.

def vendor_dashboard(request):
    pass

def vendor_signin(request):
    return render(request,'vendor_login.html')

def vendor_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        phone_number = request.POST['phone']
        GSTIN = request.POST['gstin']
        password1 = request.POST['pass-1']
        password2 = request.POST['pass-2']





        
        if first_name != first_name.capitalize():
            messages.warning(request,'First name should start with capital letter')
            return redirect(request,'vendor-signup')

        elif users.objects.filter(email = email).exists():
            messages.warning(request,'The email is already taken.')
            return redirect('vendor-signup')

        elif email:
                try:
                  validate_email(email)
                except:
                    messages.warning(request,'Enter valid email address.')
                    return redirect('vendor-signup')

        elif users.objects.filter(mobile = phone_number):
            messages.warning(request,'The phone number is already registered')
            return redirect('vendor-signup')

        elif len(phone_number) < 10:
            messages.warning(request,'Enter valid mobile number')
            return redirect('vendor-signup')
        
        elif len(GSTIN) < 15:
            messages.warning(request,'Enter valid GSTIN Number')

        elif password1 != password2:
            messages.warning(request,'Password not match with each other')
            return redirect('vendor-signup')


        

        user = users.objects.create_vendor(
                first_name = first_name,
                last_name = last_name,
                email = email,
                mobile = phone_number,
                password = password1,
                GSTIN = GSTIN

            )

        user.save()
        messages.success(request,'Registered successfully Login with Email Id and Password')

        return redirect('vendor-signin')
            
    
    return render(request,'vendor_signup.html')