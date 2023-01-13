from django.shortcuts import render,redirect
from django.contrib import messages
from user.models import users
from admin_app.models import *
from .models import Product
from django.core.validators import validate_email
from django.contrib import auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import random
from sendotp import *




# Create your views here.
@login_required(login_url='/vendor-signin')
def vendor_dashboard(request):
    return render(request,'vendor_dashboard.html')


@login_required(login_url='/vendor-signin')
def vendor_products(request):
    
    product ={
        'product':Product.objects.all()
    }
    return render(request,'vendor_product.html',product)

@login_required(login_url='/vendor-signin')
def add_product(request):

    context ={'brand':Brand.objects.all(),'categorys':Category.objects.all()}


    if request.method == 'POST':
        
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        discount_price = request.POST['discount_price']
        quantity = request.POST['stock']
        image_1 = request.FILES['img-1']
        image_2 = request.FILES['img-2']
        image_3 = request.FILES['img-3']
        category_id= request.POST['category']
        brand_id= request.POST['brand']

        category = Category.objects.filter(category_name = category_id).get(category_name = category_id)
        brand = Brand.objects.filter(brand_name = brand_id).get(brand_name = brand_id)
      





        product = Product(
         product_name = product_name,
        product_description = product_description,
        price = product_price,
        discount_price = discount_price,
        quantity = quantity,
        image_1 = image_1,
        image_2 = image_2,
        image_3 = image_3,
        category= category,
        brand = brand,
      
          )

        product.save()
        messages.success(request,'Product added successfully')
        return redirect('vendor_products')
  
    return render(request,'add_product.html',context)



@login_required(login_url='/vendor-signin')
def edit_product(request,id):

    context ={'brand':Brand.objects.all(),'categorys':Category.objects.all(),'product':Product.objects.filter(id = id)}


    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        discount_price = request.POST['discount_price']
        quantity = request.POST['stock']
        image_1 = request.FILES['img-1']
        image_2 = request.FILES['img-2']
        image_3 = request.FILES['img-3']
        category_id= request.POST['category']
        brand_id= request.POST['brand']

        category = Category.objects.filter(category_name = category_id).get(category_name = category_id)
        brand = Brand.objects.filter(brand_name = brand_id).get(brand_name = brand_id)
      





        product = Product(
            id = id,
         product_name = product_name,
        product_description = product_description,
        price = product_price,
        discount_price = discount_price,
        quantity = quantity,
        image_1 = image_1,
        image_2 = image_2,
        image_3 = image_3,
        category= category,
        brand = brand,
        time_added = datetime.now()
      
          )

        product.save()
        messages.success(request,'Product updated successfully')
        return redirect('vendor_products')
  
    return render(request,'edit_product.html',context)


@login_required(login_url='/vendor-signin')
def delete_product(request,id):
    Product.objects.filter(id = id).delete()
    messages.success(request,'Product deleted succcessfully')
    return redirect('vendor_products')



def vendor_orders(request):
    return render(request,'vendor_orders.html')


def vendor_coupon(request):
    return render(request,'vendor_coupon.html')

def vendor_offers(request):
    return render(request,'vendor_offer.html')

def vendor_salesreport(request):
    return render(request,'salesreport.html')




def vendor_signin(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        return redirect('vendor_dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        
        vendor = auth.authenticate(email = email, password = password)


        
        if vendor is not None and vendor.is_staff and vendor.is_active == True:
            auth.login(request,vendor)
            return redirect('vendor_dashboard',)
        else:
            messages.warning(request, 'Invalid password or Username')
            return redirect('vendor-signin')
    
        
    return render(request,'vendor_login.html')



def vendor_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['phone']
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

        if users.objects.filter(mobile = mobile).exists():
            messages.warning(request,'The phone number is already registered')
            return redirect('vendor-signup')

        elif len(mobile) != 10:
            messages.warning(request,'Enter valid mobile number')
            return redirect('vendor-signup')
        
        elif len(GSTIN) != 15:
            messages.warning(request,'Enter valid GSTIN Number')
            return redirect('vendor-signup')
        
        elif len(password1) < 4 :
            messages.warning(request,'Password should be of 4 or more characters')
            return redirect('vendor-signup')

        elif password1 != password2:
            messages.warning(request,'Password not match with each other')
            return redirect('vendor-signup')


        
    
        vendor = users.objects.create_vendor(
                first_name = first_name,
                last_name = last_name,
                email = email,
                mobile = mobile,
                password = password1,
                GSTIN = GSTIN

            )

        vendor.save()
        messages.success(request,'Registered successfully Login with Email Id and Password')

        return redirect('vendor-signin')
            
    
    return render(request,'vendor_signup.html')





def vendor_otp_login(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        user = users.objects.filter(mobile = mobile)
        if not user.exists():
            return redirect('vendor-signup')
        
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
        return redirect('vendor_verify_login',id)
        
            
    return render(request,'vendor_otp_login.html')





def vendor_verify_login(request,id):
    type(id)
    print(id,'8888888888888888888888888888888888')

    
    if request.method == 'POST':
        otp = request.POST['otp']
        user = users.objects.get(id = id)
        if otp == user.otps and user.is_staff == True:
            auth.login(request,user)
            return redirect('home')
        else:
          messages.info(request,'Registeryour account first and then try login')
          return redirect('vendor-signup')
    return render(request,'vendor_otp.html',{'id':id})





@login_required(login_url='/vendor-signin')
def logout(request):
    auth.logout(request)
    return redirect('vendor-signin')