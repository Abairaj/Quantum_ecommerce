from datetime import date
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
from offers.models import Offer
from orders.models import Order
from django.db.models import Count
from django.contrib.auth.hashers import make_password
from cart.forms import AddressForm
from django.db.models import Max,Min
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
# from verifyotp import verify_otp





def user_check(user):
    return not user.is_superadmin and not user.is_staff         




# Create your views here.
def home(request):
    order_count= Order.objects.values('product_id').annotate(count = Count('id')).values('product_id','count')
    cart = request.session.get('cart_id')

    product_ids = [i['product_id'] for i in order_count]
    context = {'banner':Banner.objects.all(),
               'product':Product.objects.all(),
               'variant':Variant.objects.all().order_by('-created_on')[:4],
               'offer':Offer.objects.all().order_by('-percent'),
                'top_sellers':Product.objects.filter(id__in = product_ids)[:4],
                'cart':Cart_items.objects.filter(cart = cart).count()
    }
    

    return render(request,'index.html',context)






@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_passes_test(user_check), name='dispatch')
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
    

@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_passes_test(user_check), name='dispatch')
class user_profile_edit(TemplateView):
     template_name = 'user_edit.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)

          user = users.objects.get(id = self.request.user.id)

          context['user'] = user

          return context




@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_passes_test(user_check), name='dispatch')
class user_profile_management(View):
        
    def post(self,request):
        try:
          self.request.GET['action']
        except Exception as e:
            print(e)
            action = None
        if action == None:

            image = request.FILES['image']
            # users.objects.filter(id = self.request.user.id).update(profile = image) 
            user = users.objects.get(id = self.request.user.id)
            user.profile = image
            user.save()
            
            messages.success(request,'Successfully updated the profile image')
            return redirect('user_profile')
        else:
               
               first_name = request.POST['first_name']
               last_name = request.POST['last_name']
               gender = request.POST['gender']
               email = request.POST['email']
               mobile = request.POST['mobile']



               if first_name != first_name.capitalize():
                    messages.warning(request,'First name should start with capital letter.')
                    return redirect('user_pro_edit')

               elif len(users.objects.filter(email = email)) > 1:
                    messages.warning(request,'Email is already taken')
                    return redirect('user_pro_edit')
            
               elif email:
                    try:
                        validate_email(email)
                    except:
                        messages.warning(request,'Enter valid email address.')
                        return redirect('user_pro_edit')


               if len(users.objects.filter(mobile = mobile)) > 1:
                    messages.warning(request,'The phone number is already registered')
                    return redirect('user_pro_edit')
                    
               elif len(mobile) < 10:
                        messages.warning(request,'Enter valid mobile number')
                        return redirect('user_pro_edit')
               
               user = users.objects.get(id = self.request.user.id)
               useremail = user.email

               user.first_name  = first_name
               user.last_name = last_name
               user.mobile = mobile
               user.gender = gender
               user.email = email

               user.save()

               if useremail == user.email:
                           messages.success(request,'User informations updated successfully login with new email')
                           return redirect('user_profile')
                
               else:  
                    auth.logout(request)
                    messages.success(request,'User informations updated successfully login with new email')
                    return redirect('signin')




@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_passes_test(user_check), name='dispatch')
class User_add_address_view(TemplateView):
     template_name = 'user_add_address.html'
     form_class = AddressForm

     def get_context_data(self, **kwargs):
          
          context = super().get_context_data(**kwargs)and {'form':self.form_class}
          carts = self.request.session.get('cart_id')
          cart = Cart_items.objects.filter(cart = carts).count()
          context['cart'] = cart
          return context
               
        

        


def shop(request):
    min_max_price = Variant.objects.aggregate(Min('final_price'),Max('final_price'))
    cart = request.session.get('cart_id')
  
  
    context = {'category':Category.objects.all(),'product':Product.objects.all()[:10],'variant':Variant.objects.all(),'min_max_price':min_max_price,  'cart':Cart_items.objects.filter(cart = cart).count()}

    return render(request,'shop.html',context)



def product_detail(request,id,v_id):
    product = Product.objects.get(id = id)
    variant = Variant.objects.get(id = v_id)
    cart = request.session.get('cart_id')

      
    context ={'product':Product.objects.get(id=id),'variant':Variant.objects.filter(Product = product.pk),'image':Image.objects.filter(product = id),'main_variant':Variant.objects.filter(id = v_id),'cart':Cart_items.objects.filter(cart = cart).count()}

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






@never_cache
def forgot_password(request):
     
     if request.method == 'POST':
          
          mobile = request.POST['mobile']

          if len(mobile) == 10 and users.objects.filter(mobile = mobile).exists():
               user = users.objects.filter(mobile = mobile)
               id = user[0].id
               request.session['user_id'] = mobile
               otp = str(random.randint(1000,9999))

               user.update(otps = otp)
          
               send_otp(mobile,otp)
               return redirect('forgot_otp_verify')
          else:
               messages.warning(request,'The mobile number entered by you is not valid')
               return redirect('forgetpass')
          
          
     
     return render(request,'forgotpass.html')




@never_cache
def forgot_password_verify(request):
     
     id = request.session.get('user_id')
    

     user = users.objects.get(mobile = id)
     otp_saved = user.otps

     if request.method == 'POST':
          otp = request.POST['otp']

          if otp == otp_saved:
               messages.success(request,'Change your password Here')
               return redirect('reset_password')
          else:
               messages.warning(request,'The otp entered is incorrect try again')
               return redirect('forgot_otp_verify')

     return render(request,'forgotpassword_verify.html')




@never_cache
def reset_password(request):
     if request.method == 'POST':
          
          id = request.session.get('user_id')
          user = users.objects.filter(mobile = id)
          user1 = users.objects.get(mobile =id)
          del request.session['user_id']

          pass1 = request.POST['pass1']
          pass2 = request.POST['pass2']

          if pass1 != pass2:
               messages.warning(request,'Password not matches with each other')
               return redirect('reset_password')
          
          else:
               user.update(password = make_password(pass1))
               if user1.is_staff == True:
                    messages.success(request,'password changed successfully. .Sign in with the new password')
                    return redirect('vendor-signin')
               else:  
                  messages.success(request,'password changed successfully. .Sign in with the new password')
                  return redirect('signin')
          
     return render(request,'resetpassword.html')
          
     





@never_cache
def otp_login(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        user = users.objects.filter(mobile = mobile)
        if not user.exists():
            return redirect('signup')
        
        print(user[0])
        print(user[0].otps)
        otp_r = str(random.randint(1000,9999))
        print(otp_r)
        # user[0].otps = otp_r
        user.update(otps = otp_r)

        print(user[0].otps)
        user[0].save() 
        id = user[0].id
        send_otp(mobile,user[0].otps)
        return redirect('verify_login',id)
        
            
    return render(request,'otp_login.html')







@never_cache
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



def product_list_ajax(request):
     products = Product.objects.all().values_list('product_name',flat=True)
     product_list = list(products)
     category = Category.objects.all().values_list('category_name',flat=True) 

     category = list(category)         
           
     product_list.extend(category)


     return JsonResponse(product_list,safe=False)




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
     template_name = 'shop.html'

     def get_context_data(self, **kwargs):
          
        try:
          action = self.request.GET.get('price')
        except Exception as e:
          print(e)
          action= None

        if action == None:
          id = kwargs.get('id')
          context =  super().get_context_data(**kwargs)
          #found product id using category id
          product = Product.objects.filter(category = id)
          #list comprehension to add all the product_id in a list
          product_ids = [product.pk for product in product]
          #checked the list using __in  for matching vriants and filer is done
          variant = Variant.objects.filter(Product__in = product_ids)

          all_categories = Category.objects.all()

          min_max_price = Variant.objects.aggregate(Min('final_price'),Max('final_price'))

         
          context['variant'] = variant
          context['product'] = product
          context["category"] = all_categories
          context['min_max_price'] = min_max_price


          return context
        

def brand_filter(request,id):
    try:
        Brand.objects.get(id = id)
        product = Product.objects.filter(brand  = id)
        productids = [i for i in product]
        variant = Variant.objects.filter(Product__in = productids)
    except:   
       variant = Variant.objects.filter(Product = id)
     
    min_max_price = Variant.objects.aggregate(Min('final_price'),Max('final_price'))

    context = {'variant':variant,'min_max_price':min_max_price,'category':Category.objects.all()}

    return render (request,'shop.html',context)

        






def filter(request):
    min_max_price = Variant.objects.aggregate(Min('final_price'),Max('final_price'))
    action = request.GET.get('action')
    if action == 'popularity':
        item = Order.objects.annotate(times=Count('Variant')).values('Variant', 'times').order_by('-times')
        variant_ids = [item['Variant'] for item in item]
        variants = Variant.objects.filter(id__in=variant_ids)
        all_categories = Category.objects.all()
        context = {'variant': variants,'category':all_categories,'min_max_price':min_max_price}
        return render(request, 'shop.html', context)


    elif request.method == 'POST':
          max_price = request.POST['max_price']
          min_price = request.POST['min_price']

          variant = Variant.objects.filter(Q(final_price__gte = min_price) and Q(final_price__lte = max_price))
          all_categories = Category.objects.all()
          context = {'variant':variant,'category':all_categories,'min_max_price':min_max_price}
          return render(request,'shop.html',context)
    else:
         return render(request,'shop.html')
                       
         
          
# ===================================================================================Wallet=========================================================================

@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(user_passes_test(user_check), name='dispatch')
class Wallet_view(TemplateView):
     template_name = 'wallet.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)

          wallet = Wallet.objects.filter(user_id = self.request.user.id)
          context['wallet'] = wallet
          cart = self.request.session.get('cart_id')
          context['cart'] = Cart_items.objects.filter(cart = cart).count()

          return context






@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('home')