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
from django.views.generic import TemplateView,View
from sendotp import *
from cart.models import *
from django.http import JsonResponse

# from serializers import ChangepasswordSerializers
# from rest_framework.permissions import IsAuthenticated
# from verifyotp import verify_otp



            



# Create your views here.
def home(request):
    context = {'banner':Banner.objects.all,'product':Product.objects.all(),'variant':Variant.objects.all().order_by('-created_on')[:4]}

    return render(request,'index.html',context)





class user_profile(TemplateView):
    template_name = 'user_profile.html'
    def get_context_data(self, **kwargs):
        user = self.request.user.id
        context =  super().get_context_data(**kwargs)
        user = users.objects.get(id = user)
        try:
         address = Address.objects.get(user = user)
         context["address"] = address
        except Exception as e:
         print(e)
        context['user'] = user

        return context
    

    
class user_profile_management(View):
        
        def post(self,request):

            image = request.FILES['image']
            users.objects.filter(id = self.request.user.id).update(profile = image) 
            messages.success(request,'Successfully updated the profile image')
            return redirect('user_profile')
        


def shop(request):
    context = {'category':Category.objects.all(),'product':Product.objects.all()[:10],'variant':Variant.objects.all()}
    return render(request,'shop.html',context)



def product_detail(request,id,v_id):
    product = Product.objects.get(id = id)
    variant = Variant.objects.get(id = v_id)
      
    context ={'product':Product.objects.get(id=id),'variant':Variant.objects.filter(Product = product.pk),'image':Image.objects.filter(product = id),'main_variant':variant}

    varian = Variant.objects.filter(Product = product.pk)

    

  

    print(context)

    return render(request,'product-detail.html',context)






@never_cache
def signin(request):

    if request.user.is_authenticated and request.user.is_staff == False:
        messages.success(request,'You have already signed in. ')
        return redirect('home')


    elif request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        


        user = auth.authenticate(email = email,password = password)
        
        if user is not None and user.is_active == True and user.is_staff == False:

            cart = Cart.objects.get(user_id = user.id)
            request.session['cart_id'] = str(cart)
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

                id = users.objects.get(id = user.id)

                cart = Cart.objects.create(
                     user_id = id,
                     total = 0
                )
                
                cart.save()
                request.session['cart_id'] = str(cart)
                print(request.session.get('cart_id'))

                wallet = Wallet.objects.create(
                     user_id = users.objects.get(id = user.id)
                )

                wallet.save()
            

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
    
    if request.method == 'POST':
        otp = request.POST['otp']
        user = users.objects.get(id = id)
        if otp == user.otps:
            login(request,user)
            return redirect('home')
        else:
          return redirect('signup')
    return render(request,'otp.html',{'id':id})


# ====================================================================Searchbar ===============================================

def search_bar(request):
          categories = Category.objects.all()
          if request.method == 'GET':
               search =request.GET['search']

               if search:
                  try:
                    product = Product.objects.filter(product_name__icontains = search)
                    #searching by product
                    if product:
                        product_ids = [product for product in product]
                        variant = Variant.objects.filter(Product__in = product_ids)

                        variants = {
                            'variant':variant ,
                            'category':categories
                        }
                        return render(request,'shop.html',variants)
                    category = Category.objects.filter(category_name__icontains = search)
                    #searching by category
                    if category:
                         category_ids = [category for category in category]
                         product2 = Product.objects.filter(category_id__in = category_ids)
                         product_ids2 = [product2 for product2 in product2]
                         variant2 = Variant.objects.filter(Product__in = product_ids2)
                         variants2 = {
                              'variant':variant2,
                               'category':categories
                         }
                         return render(request,'shop.html',variants2)
                  except Exception as e:
                        print(e)
          
          return redirect('shop')




class Category_filter(TemplateView):
     template_name = 'Category _filter.html'

     def get_context_data(self, **kwargs):
          id = kwargs.get('id')
          context =  super().get_context_data(**kwargs)
          #found product id using category id
          product = Product.objects.filter(category = id)
          #list comprehension to add all the product_id in a list
          product_ids = [product.pk for product in product]
          #checked the list using __in  for matching vriants and filer is done
          variant = Variant.objects.filter(Product__in = product_ids)

          all_categories = Category.objects.all()

         
          context['variant'] = variant
          context['product'] = product
          context["all_category"] = all_categories

          return context
                       
         
          
# ===================================================================================Wallet=========================================================================

class Wallet_view(TemplateView):
     template_name = 'wallet.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)

          wallet = Wallet.objects.all()
          context['wallet'] = wallet

          return context





          
               




@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('home')