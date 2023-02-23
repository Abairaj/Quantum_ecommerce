from django.shortcuts import render,redirect
from django.contrib import messages
from user.models import users
from admin_app.models import *
from .models import Product,Color,Variant,Image
from cart.models import Coupon
from django.core.validators import validate_email
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic import View,TemplateView
import random
from sendotp import *
from orders.models import Order
from django.utils.decorators import method_decorator
import io
from django.http import FileResponse
import openpyxl
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.db.models import Q
from datetime import datetime
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from cart.models import Cart_items



def vendor_check(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff == True and request.user.is_superadmin == False:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('vendor-signin')
    return wrapper_func





@never_cache
@login_required(login_url='/vendor-signin')
@vendor_check
def vendor_dashboard(request):
  
    vendor_id = users.objects.get(id = request.user.id)
    product = Product.objects.filter(vendor_name = vendor_id)
    product_ids = [i.pk for i in product]
    order = Order.objects.filter(product_id__in = product_ids).filter(is_active = 'True')
    cancelled_order = Order.objects.filter(product_id__in = product_ids).filter(status = 'Cancelled')



    
    if order:

        total_amount = 0
        count = 0
        for i in order:
            total_amount += i.amount
            count += 1

        total_cancelled_orders = 0

        for i in cancelled_order:
            total_cancelled_orders+=1
        # total orders
        date_to_total_orders = {}
        date_of_order = []

        


        orders = order.filter(product_id__vendor_name=vendor_id)
        annotated_orders = orders.annotate(date=Trunc('order_date', 'day', output_field=DateTimeField()))
        final_orders = annotated_orders.annotate(count=Count('id')).values('date','count')

        for i in final_orders:
            date = i['date'].strftime("%Y-%m-%d")
            if date in date_to_total_orders:
                date_to_total_orders[date] += i['count']
            else:
                date_to_total_orders[date] = i['count']
                date_of_order.append(date)


        
        #cancelled orders

        date_to_cancelled_orders = {}
        date_of_cancelled_order = []

        


        orders = cancelled_order.filter(product_id__vendor_name=vendor_id)
        annotated_orders = orders.annotate(date=Trunc('order_date', 'day', output_field=DateTimeField()))
        final_orders = annotated_orders.annotate(count=Count('id')).values('date','count')

        for i in final_orders:
            date = i['date'].strftime("%Y-%m-%d")
            if date in date_to_cancelled_orders:
                date_to_cancelled_orders[date] += i['count']
            else:
                date_to_cancelled_orders[date] = i['count']
                date_of_cancelled_order.append(date)

        print(date_of_cancelled_order)
        current_year =  datetime.now().year

        context = {'date_to_total_orders':date_to_total_orders,
                'date_of_order':date_of_order,
                'current_year':current_year,
                'date_of_cancelled_order':date_of_cancelled_order,
                'date_to_cancelled_orders':date_to_cancelled_orders,
                'total_revenue':total_amount,
                'total_order':count,
                'total_cancelled_orders':total_cancelled_orders,
                'cancelled_order78':cancelled_order.count(),
                'order78':order.count()
                }
        

        return render( request,'vendor_dashboard.html',context)
    else:
         return render(request, 'vendor_dashboard.html', {})





@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class Vendor_profile(TemplateView):
    template_name = 'vendor_profile.html'
    def get_context_data(self, **kwargs):
        user = self.request.user.id
        context =  super().get_context_data(**kwargs)
        vendor = users.objects.get(id = user)
        try:
         address = Address.objects.get(user = user)
         context["address"] = address
        except Exception as e:
         print(e)
        context['vendor'] = vendor

        return context
    



@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class vendor_profile_edit(TemplateView):
     template_name = 'vendor_profile_edit.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)

          user = users.objects.get(id = self.request.user.id)

          context['user'] = user

          return context

    
    


@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch') 
@method_decorator(vendor_check, name='dispatch')
class Vendor_profile_management(View):
        
        def post(self,request):
          
                if self.request.GET['action'] != 'fullchange':

                    image = request.FILES['image']
                    # users.objects.filter(id = self.request.user.id).update(profile = image) 
                    user = users.objects.get(id = self.request.user.id)
                    user.profile = image
                    user.save()
                    
                    messages.success(request,'Successfully updated the profile image')
                    return redirect('vendor_profile')
                else:
                    
                    first_name = request.POST['first_name']
                    last_name = request.POST['last_name']
                    gender = request.POST['gender']
                    email = request.POST['email']
                    mobile = request.POST['mobile']



                    if first_name != first_name.capitalize():
                            messages.warning(request,'First name should start with capital letter.')
                            return redirect('vendor_pro_edit')

                    elif len(users.objects.filter(email = email)) > 1:
                            messages.warning(request,'Email is already taken')
                            return redirect('vendor_pro_edit')
                    
                    elif email:
                            try:
                                validate_email(email)
                            except:
                                messages.warning(request,'Enter valid email address.')
                                return redirect('vendor_pro_edit')


                    if len(users.objects.filter(mobile = mobile)) > 1:
                            messages.warning(request,'The phone number is already registered')
                            return redirect('vendor_pro_edit')
                            
                    elif len(mobile) < 10:
                                messages.warning(request,'Enter valid mobile number')
                                return redirect('vendor_pro_edit')
                
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
                                return redirect('vendor_profile')
                        
                    else:  
                            auth.logout(request)
                            messages.success(request,'User informations updated successfully login with new email')
                            return redirect('vendor-signin')





@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class Vendor_wallet(TemplateView):
    template_name = 'vendor_wallet.html'

    def get_context_data(self, **kwargs):
       context =  super().get_context_data(**kwargs)

       wallet = Wallet.objects.filter(user_id = self.request.user.id)
       context['wallet'] = wallet
       return context




@login_required(login_url='/vendor-signin')
@vendor_check
def vendor_products(request):
    vendor = request.user
    id = vendor.id
    product ={
        'product':Product.objects.all().filter(vendor_name = id)
    }
    return render(request,'vendor_product.html',product)




@login_required(login_url='/vendor-signin')
@vendor_check
def add_product(request):

    context ={'brand':Brand.objects.all(),'categorys':Category.objects.all()}


    if request.method == 'POST':
        
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        category_id= request.POST['category']
        brand_id= request.POST['brand']
        images = request.FILES.get('image')
        color = str(request.POST['color'])
        max_price = request.POST['price']
        max_discount = request.POST['discount']
        final_price = float(max_price) - (float(max_discount)/100)*float(max_price)
        category = Category.objects.get(category_name = category_id)
        brand = Brand.objects.get(brand_name = brand_id)
        vendor_id = users.objects.get(id = request.user.id)
        colors = color.split(',')




    # Creating new product and adding colours 
        product = Product(
         product_name = product_name,
        product_description = product_description,
        category= category,
        brand = brand,
        vendor_name = vendor_id,
        product_image = images,
        max_price = max_price,
        max_discount = max_discount,
        final_price = final_price

      
          )

        product.save()

        for i in colors:
            colour = Color (
                product = Product.objects.get(id = product.pk),
                name = i

            )

            colour.save()


        messages.success(request,'Product added successfully')
        return redirect('vendor_products')
  
    return render(request,'add_product.html',context)



@login_required(login_url='/vendor-signin')
@vendor_check
def edit_product(request,id):

    colors = []


    context ={'brand':Brand.objects.all(),'categorys':Category.objects.all(),'product':Product.objects.filter(id = id),'colour':Color.objects.filter(product = id)}


    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        category_id= request.POST['category']
        brand_id= request.POST['brand']
        max_price = request.POST['price']
        max_discount = request.POST['discount']
        final_price = float(max_price) - (float(max_discount)/100)*float(max_price)
        image = request.FILES.get('image')
        colors = []

        for i in Color.objects.filter(product = id):
            print(i.id)
            g = request.POST[f'color{i.id}']
            print(g)
            colors.append(g)
        
        
        colors = iter(colors)
        
        print(colors)


        category = Category.objects.get(category_name = category_id)
        brand = Brand.objects.get(brand_name = brand_id)
        vendor_id = users.objects.get(id = request.user.id)        
        
      



# updating the products created earlier
        if image:
            product = Product(
                id = id,
            product_name = product_name,
            product_description = product_description,
            category= category,
            max_price = max_price,
            max_discount  = max_discount,
            final_price = final_price,
            brand = brand,
            vendor_name = vendor_id,
            product_image = image,
            time_added = datetime.now()
        
            )

            product.save()
        else:
            product = Product.objects.filter(id = id)
            product.update(
                id = id,
            product_name = product_name,
            product_description = product_description,
            category= category,
            max_price = max_price,
            max_discount  = max_discount,
            final_price = final_price,
            brand = brand,
            vendor_name = vendor_id,
            time_added = datetime.now()
        
            )
        
        p = Product.objects.get(id = id)

        colour_id = Color.objects.filter(product = p.pk)
        
        for i in colour_id:
                colour = Color(
                    id = i.id,
                    product = Product.objects.get(id = p.pk),
                    name = next(colors)
                    
                )

                colour.save()
        messages.success(request,'Product updated successfully')
        return redirect('vendor_products')
  
    return render(request,'edit_product.html',context)



# deleting the product
@login_required(login_url='/vendor-signin')
@vendor_check
def delete_product(request,id):
    Product.objects.filter(id = id).delete()
    messages.success(request,'Product deleted succcessfully')
    return redirect('vendor_products')



# ===============================================================Variants==========================================================

#view product cards and go to variant of paricular product
@login_required(login_url='/vendor-signin')
@vendor_check
def variant_view(request):
    product = {
        'product':Product.objects.all().filter(vendor_name = request.user.id)
    }
    return render(request,'variant_view.html',product)


#variant view of a product 
@login_required(login_url='/vendor-signin')
@vendor_check
def variant(request,id):
    product=Product.objects.get(id = id)
    variant =Variant.objects.filter(Product = id)
    variants = {
        'variant':variant,'product':product
                                         }

    return render(request,'variants.html',variants)




#   Add a new variant
@login_required(login_url='/vendor-signin')
@vendor_check
def add_variants(request,id):
    product = Product.objects.get(id = id)
    context = {
        'product':product,'color':Color.objects.filter(product = id)
    }

    if request.method == 'POST':
        color = request.POST['color']
        price = request.POST['price']
        discount = request.POST['discount']
        quantity = request.POST['stock']
        images = request.FILES.getlist('images')
   

        colour = Color.objects.filter(product = id).get(name = color)
        print(colour)
        
        if float(price) > float(product.max_price):
            messages.warning(request,f'Price can\'t be greater than {product.max_price}.Make changes in product and try again ')
            return redirect('add_variant',id)
        if float(discount) > float(product.max_discount):
            messages.warning(request,f'Discount more than {product.max_discount} is not possible.Make changes in product and try again')
            return redirect('add_variant',id)








        variant = Variant.objects.create(
                Product = Product.objects.get(id = id),
                color = colour,
                price = price,
                discount_percentage = discount,
                quantity = quantity,
                final_price = float(price) - (float(discount) / 100) * float(price) 
                                            
            )



        for i in reversed(images):
            image = Image.objects.create(
                product = Product.objects.get(id = id),
                variant = Variant.objects.get(id = variant.pk),
                image = i,
            )
    
         


        messages.success(request,'Product added successfully')
        return redirect('vendor_variant',product.pk)

    return render(request,'add_variant.html',context)


#Edit a new variant

@login_required(login_url='/vendor-signin')
@vendor_check
def edit_variant(request,id):
    variants = Variant.objects.get(id = id)
    product = variants.Product
    context = {
        'variant':Variant.objects.filter(id = id), 'color':Color.objects.filter(product = variants.Product.pk)
    }


    if request.method == 'POST':
        color = request.POST['color']
        price = request.POST['price']
        discount = request.POST['discount']
        quantity = request.POST['stock']
        image1 = request.FILES.getlist('images')
        colour = Color.objects.filter(product = variants.Product.pk).get(name = color)
  
    

        

        if float(price) > (product.max_price):
            messages.warning(request,f'Price can\'t be greater than {product.max_price}.Make changes in product and try again ')
            return redirect('add_variant',id)
        if float(discount) > float(product.max_discount):
            messages.warning(request,f'Discount more than {product.max_discount} is not possible.Make changes in product and try again')
            return redirect('add_variant',id)




        variant = Variant(
            id = id,
            Product = Product.objects.get(id = variants.Product.pk),
            color = colour,
            price = price,
            discount_percentage = discount,
            quantity = quantity,
            final_price = float(price) - (float(discount) / 100) * float(price) 
                                          
        )

        variant.save()

        print(Image.objects.values_list('variant'))
        img = Image.objects.filter(variant = id)


     
        image_ids = [i.pk for i in img]


     

        for image, id in zip(reversed(image1), image_ids):
              
                img = Image(
                    id = Image.objects.get(id = id).pk,
                    image = image,
                    variant = Variant.objects.get(id = variant.pk),
                    product = Product.objects.get(id = product.pk)
                )

                img.save()
            
            
            

        messages.success(request,'Variant updated successfully')

        return redirect('vendor_variant',product.pk)

    return render(request,'edit_variant.html',context)



#delete a variant
@login_required(login_url='/vendor-signin')
@vendor_check
def delete_variants(request,id):
    variant = Variant.objects.get(id = id)
    variant.delete()

    messages.success(request,'Variant deleted successfully')
    return redirect('vendor_variant',variant.Product.pk)







#=============================================================vendor authentication signin,signup==============================================
@never_cache
def vendor_signin(request):
    if request.user.is_staff == True and request.user.is_superadmin == False:
        return redirect('vendor_dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        
        vendor = auth.authenticate(email = email, password = password)


        
        if vendor is not None and vendor.is_staff and vendor.is_active == True:
            auth.login(request,vendor)
            return redirect('vendor_dashboard')
        else:
            messages.warning(request, 'Invalid password or Username')
            return redirect('vendor-signin')
    
    cart = request.session.get('cart_id')
    context = {'cart':Cart_items.objects.filter(cart = cart).count()}
    return render(request,'vendor_login.html',context)


@never_cache
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

        wallet = Wallet(
            user_id = users.objects.get(id = vendor.id),
            balance = 0
        )
        wallet.save()
        messages.success(request,'Registered successfully Login with Email Id and Password')

        return redirect('vendor-signin')
            
    cart = request.session.get('cart_id')
    context = {'cart':Cart_items.objects.filter(cart = cart).count()}
    return render(request,'vendor_signup.html',context)



#===============================================================================OTP Login and verification==============================================================
@never_cache
def vendor_otp_login(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        user = users.objects.filter(mobile = mobile)
        if not user.exists():
            return redirect('vendor-signup')
        
        otp_r = str(random.randint(1000,9999))
        user.update(otps = otp_r)

        print(user[0].otps)
        user[0].save() 
        id = user[0].id
        send_otp(mobile,user[0].otps)
        return redirect('vendor_verify_login',id)
        
            
    return render(request,'vendor_otp_login.html')




@never_cache
def vendor_verify_login(request,id):
    type(id)
    
    if request.method == 'POST':
        otp = request.POST['otp']
        user = users.objects.get(id = id)
        if otp == user.otps and user.is_staff == True:
            auth.login(request,user)
            return redirect('home')
        else:
          messages.info(request,'Register your account first and then try login')
          return redirect('vendor-signup')
    return render(request,'vendor_otp.html',{'id':id})




        



#=======================================================Vendor Order management============================================================


@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class Order_management(TemplateView):
    template_name = 'vendor_orders.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        vendor_id = users.objects.get(id = self.request.user.id)
        product = Product.objects.filter(vendor_name = vendor_id)
        order = Order.objects.filter(is_active = 'True')
        
        for i in order:
           if i.product_id.vendor_name == vendor_id:
                if order:
                        context['order'] = order
                        return context





@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class Update_order_status(View):
    
    def post(self,request,**kwargs):

        id = self.kwargs.get('id')
        status = request.POST['status']

        order = Order.objects.get(id = id)

        order.status = status
        order.save()
        return redirect('vendor_orders')
        
        
#=========================================================vendor coupon management=============================================================

#coupon main page
@login_required(login_url='/vendor-signin')
@vendor_check
def vendor_coupon(request):
    context = {
        'coupon':Coupon.objects.all()
    }
    return render(request,'vcoupon.html',context)




# add coupon

@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class add_coupon(View):
    def post(self,request):
        code = request.POST['code']
        expiry = request.POST['expiry']
        minimum_amount = request.POST['minimum_amount']
        discount_price = request.POST['discount_price']
        expiry =  datetime.strptime(expiry, "%m/%d/%Y")
        expiry.strftime("%Y-%m-%d")

        coupon = Coupon(
            coupon_code = code,
            expiry_date = expiry,
            minimum_amount = minimum_amount,
            discount_price = discount_price
        )

        coupon.save()
        messages.warning(request,'Coupon added successfully')
        return redirect('vendor_coupon')
    



# delete coupon
@login_required(login_url='/vendor-signin')
@vendor_check
def activate_coupon(request,id):
    coupon = Coupon.objects.get(id = id)
    coupon.expired = False
    coupon.save()
    messages.success(request,'Coupon Activated successfully')
    return redirect('vendor_coupon')


@login_required(login_url='/vendor-signin')
@vendor_check
def deactivate_coupon(request,id):
    coupon = Coupon.objects.get(id = id)
    coupon.expired = True
    coupon.save()
    messages.success(request,'Coupon Deactivated successfully')
    return redirect('vendor_coupon')


# edit coupon
@login_required(login_url='/vendor-signin')
@vendor_check
def edit_coupon(request,id):
    if request.method == 'POST':

        code = request.POST['code']
        expiry = request.POST['expiry']
        minimum_amount = request.POST['minimum_amount']
        discount_price = request.POST['discount_price']
        expiry =  datetime.strptime(expiry, "%Y-%m-%d")
        expiry.strftime("%Y-%m-%d")
        coupon = Coupon(
            id = id,
            coupon_code = code,
            expiry_date = expiry,
            minimum_amount = minimum_amount,
            discount_price = discount_price


        )
        coupon.save()

        messages.success(request,'Coupon updated successfully')
        return redirect('vendor_coupon')


# ===========================================================================================sales report===================================================================

@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class Vendor_Salesreport_view(TemplateView):
    template_name = 'vendor_salesreport.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.user

        product = Product.objects.filter(vendor_name = id.id)

        product_ids = [product for product in product]

        order = Order.objects.all().filter(product_id__in = product_ids).order_by('order_date')

        context['order'] = order

        return context
    




@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class vendor_Salesreport_download(View):


    def get(self,request):
       id = self.request.user

       product = Product.objects.filter(vendor_name = id.id)

       product_ids = [product for product in product] 
       try:
        start_str = self.request.GET.get('start')
        end_str = self.request.GET.get('end')
        start = datetime.strptime(start_str, '%Y-%m-%d').date()
        end = datetime.strptime(end_str, '%Y-%m-%d').date()
       except Exception as e:
          print(e)
          start = None
          
       if start:

           order = Order.objects.filter(Q(order_date__gte = start) & Q (order_date__lte = end)).filter(product_id__in = product_ids).order_by('order_date')    
           
       else:
           order = Order.objects.all().filter(product_id__in = product_ids).order_by('order_date')


       
       #pdf
       if 'excel' not in request.GET:


                buffer = BytesIO()
            
                # Create the PDF object
                pdf = SimpleDocTemplate(buffer, title = 'Sales report')

                #  data for the table
                data = []
                header = ["Order Date", "Order ID", "Category", "Brand", "Sales Amount"]
                data.append(header)

                for report in order:
                    data.append([str(report.order_date.date()), str(report.id), report.product_id.category.category_name, report.product_id.brand.brand_name, str(report.amount)])

                # Creating  the table
                table = Table(data, colWidths=[100, 100, 100, 100, 100], rowHeights=30)

                table.setStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ])


                # page heading
                styles = getSampleStyleSheet()
                heading = Paragraph("Sales Report", style=styles["Heading1"])

                # writing the table in the pdf
                pdf.build([heading, table])

                # Close the PDF object
                buffer.seek(0)
                
                # Get the value of the PDF file from the buffer
                pdf = buffer.getvalue()

                # Return the PDF file through Django's FileResponse
                response = FileResponse(BytesIO(pdf), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
                return response




            # excel
       else:

                # Creating a new Excel workbook
                    workbook = openpyxl.Workbook()

                    # Selecting the active worksheet
                    worksheet = workbook.active

                    # the headers to the worksheet
                    worksheet['A1'] = "Order Date"
                    worksheet['B1'] = "Order ID"
                    worksheet['D1'] = "Category"
                    worksheet['E1'] = "Brand"
                    worksheet['C1'] = "Sales Amount"


                    #  sales report data to the worksheet
                    for row, report in enumerate(order, start=2):
                        worksheet.cell(row=row, column=1, value= str(report.order_date.date()))
                        worksheet.cell(row=row, column=2, value= str(report.id))
                        worksheet.cell(row=row, column=4, value=report.product_id.category.category_name)
                        worksheet.cell(row=row, column=5, value=report.product_id.brand.brand_name)
                        worksheet.cell(row=row, column=3, value= str(report.amount))


                # Create a file-like buffer to receive Excel workbook data
                    buffer = io.BytesIO()

                    # Save the workbook to the buffer
                    workbook.save(buffer)

                    # FileResponse sets the Content-Disposition header so that browsers
                    # present the option to save the file.
                    buffer.seek(0)
                    return FileResponse(buffer, as_attachment=True,filename='sales_report.xlsx')






@method_decorator(login_required(login_url='/vendor-signin'), name='dispatch')
@method_decorator(vendor_check, name='dispatch')
class salesreport_filter(View):

    def post(self,request):

        start_str = request.POST['from']
        end_str = request.POST['to']

        start =  datetime.strptime(start_str, '%Y-%m-%d').date()
        end =  datetime.strptime(end_str, '%Y-%m-%d').date()
        try:
          order = Order.objects.filter(Q(order_date__gte = start) & Q (order_date__lte = end)).order_by('order_date')
          return render(request,'vendor_salesreport.html',{'order':order,'start':start_str,'end':end_str})
        except Exception as e:
            print(e)
            messages.warning(request,'Try with proper values')
            return redirect('vendor_sales_report')
       
    





@login_required(login_url='/vendor-signin')
def logout(request):
    auth.logout(request)
    return redirect('vendor-signin')