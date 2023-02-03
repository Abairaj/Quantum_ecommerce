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
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.db.models import Q,F
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.cache import never_cache




# Create your views here.
@never_cache
@login_required(login_url='/vendor-signin')
def vendor_dashboard(request):
  vendor_id = users.objects.get(id = request.user.id)
  product = Product.objects.filter(vendor_name = vendor_id)
  order = Order.objects.filter(is_active = 'True')
  
  selected_date = request.POST.get('selected_date', None)
  
  if selected_date:
    order = order.filter(order_date__date=selected_date)
  
  if order:
    total_order = []
    date_of_order = []

    from django.db.models import Count, DateTimeField
    from django.db.models.functions import Trunc

    orders = order.filter(product_id__vendor_name=vendor_id)
    annotated_orders = orders.annotate(date=Trunc('order_date', 'day', output_field=DateTimeField()))
    final_orders = annotated_orders.annotate(count=Count('id')).values('date','count')

    for i in final_orders:
      total_order.append(i['count'])
      date_of_order.append(i['date'].strftime("%Y-%m-%d"))

    return render( request,'vendor_dashboard.html',{'total_order':total_order,'date_of_order':date_of_order})
  else:

    return render(request, 'vendor_dashboard.html', {})



           
        # return render(request,'vendor_dashboard.html',{'monthNumber':date_of_order,'totalOrder':total_order,'cancelled_month':[0],'cancelled_order':[0]})





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
    



class vendor_profile_edit(TemplateView):
     template_name = 'vendor_profile_edit.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)

          user = users.objects.get(id = self.request.user.id)

          context['user'] = user

          return context

    
    

    
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





class Vendor_wallet(TemplateView):
    template_name = 'vendor_wallet.html'

    def get_context_data(self, **kwargs):
       context =  super().get_context_data(**kwargs)

       wallet = Wallet.objects.get(user_id = self.request.user.id)
       context['wallet'] = wallet
       return context
















@login_required(login_url='/vendor-signin')
def vendor_products(request):
    vendor = request.user
    id = vendor.id
    product ={
        'product':Product.objects.all().filter(vendor_name = id)
    }
    return render(request,'vendor_product.html',product)

@login_required(login_url='/vendor-signin')
def add_product(request):

    context ={'brand':Brand.objects.all(),'categorys':Category.objects.all()}


    if request.method == 'POST':
        
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        category_id= request.POST['category']
        brand_id= request.POST['brand']
        images = request.FILES['image']
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
        image = request.FILES['image']
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

        colour_id = Color.objects.filter(product = product.pk)
        
        for i in colour_id:
                colour = Color(
                    id = i.id,
                    product = Product.objects.get(id = product.pk),
                    name = next(colors)
                    
                )

                colour.save()
        messages.success(request,'Product updated successfully')
        return redirect('vendor_products')
  
    return render(request,'edit_product.html',context)



# deleting the product
@login_required(login_url='/vendor-signin')
def delete_product(request,id):
    Product.objects.filter(id = id).delete()
    messages.success(request,'Product deleted succcessfully')
    return redirect('vendor_products')



# ===============================================================Variants==========================================================

#view product cards and go to variant of paricular product
@login_required(login_url='/vendor-signin')
def variant_view(request):
    product = {
        'product':Product.objects.all().filter(vendor_name = request.user.id)
    }
    return render(request,'variant_view.html',product)


#variant view of a product 
@login_required(login_url='/vendor-signin')
def variant(request,id):
    product=Product.objects.get(id = id)
    variant =Variant.objects.filter(Product = id)
    variants = {
        'variant':variant,'product':product
                                         }

    return render(request,'variants.html',variants)




#   Add a new variant
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
        image_1 = request.FILES['image-1']
        image_2 = request.FILES['image-2']
        image_3 = request.FILES['image-3']
    

        colour = Color.objects.filter(product = id).get(name = color)
        print(colour)
        
        if float(price) > float(product.max_price):
            messages.warning(request,f'Price can\'t be greater than {product.max_price}.Make changes in product and try again ')
            return redirect('add_variant',id)
        if float(discount) > float(product.max_discount):
            messages.warning(request,f'Discount more than {product.max_discount} is not possible.Make changes in product and try again')
            return redirect('add_variant',id)




        images = Image.objects.create(
            product = Product.objects.get(id = id),
            image_1 = image_1,
            image_2 = image_2,
            image_3 = image_3,
    
        )



        variant = Variant.objects.create(
            Product = Product.objects.get(id = id),
            color = colour,
            price = price,
            discount_percentage = discount,
            quantity = quantity,
            image = Image.objects.get( id=images.pk),
            final_price = float(price) - (float(discount) / 100) * float(price) 
                                          
        )


        messages.success(request,'Product added successfully')
        return redirect('add_variant',id)

    return render(request,'add_variant.html',context)


#Edit a new variant

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
        image_1 = request.FILES['image-1']
        image_2 = request.FILES['image-2']
        image_3 = request.FILES['image-3']
        colour = Color.objects.filter(product = variants.Product.pk).get(name = color)
        img = Image.objects.get(id = variants.image.pk)
    

        

        if float(price) > (product.max_price):
            messages.warning(request,f'Price can\'t be greater than {product.max_price}.Make changes in product and try again ')
            return redirect('add_variant',id)
        if float(discount) > float(product.max_discount):
            messages.warning(request,f'Discount more than {product.max_discount} is not possible.Make changes in product and try again')
            return redirect('add_variant',id)


        


                
        # imageid = Image.objects.get(product =  variants.Product.pk)
        print(Image.objects.get(pk = id).id)
        img_id = Image.objects.get(id = variants.image.id)


        images = Image.objects.filter(pk =variants.image.id)        
        images.update( 
            id = img_id.id,
            product = Product.objects.get(id =variants.Product.pk),
            image_1 = image_1,
            image_2 = image_2,
            image_3 = image_3,
        )


       
        variant = Variant(
            id = id,
            Product = Product.objects.get(id = variants.Product.pk),
            color = colour,
            price = price,
            discount_percentage = discount,
            image = images.get(id = variants.image.pk),
            quantity = quantity,
            final_price = float(price) - (float(discount) / 100) * float(price) 
                                          
        )

        variant.save()

        messages.success(request,'Variant updated successfully')

        return redirect('edit_variant',variants.pk)

    return render(request,'edit_variant.html',context)



#delete a variant

def delete_variants(request,id):
    variant = Variant.objects.get(id = id)
    variant.delete()

    messages.success(request,'Variant deleted successfully')
    return redirect('vendor_variant',variant.Product.pk)







#=============================================================vendor authentication signin,signup==============================================
def vendor_signin(request):
    if request.user.is_authenticated:
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



#===============================================================================OTP Login and verification==============================================================

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

@method_decorator(login_required(login_url='signin'), name='dispatch')
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
def vendor_coupon(request):
    context = {
        'coupon':Coupon.objects.all()
    }
    return render(request,'vendor_coupon.html',context)




# add coupon
class add_coupon(View):
    def post(self,request):
        code = request.POST['code']
        expiry = request.POST['expiry']
        minimum_amount = request.POST['minimum_amount']
        discount_price = request.POST['discount_price']

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
def delete_coupon(request,id):
    coupon = Coupon.objects.get(id = id)
    coupon.delete()
    messages.success(request,'Coupon deleted successfully')
    return redirect('vendor_coupon')


# edit coupon
def edit_coupon(request,id):
    if request.method == 'POST':

        code = request.POST['code']
        expiry = request.POST['expiry']
        minimum_amount = request.POST['minimum_amount']
        discount_price = request.POST['discount_price']

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

class Vendor_Salesreport_view(TemplateView):
    template_name = 'vendor_salesreport.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id = self.request.user

        product = Product.objects.filter(vendor_name = id.id)

        product_ids = [product for product in product]

        order = Order.objects.all().filter(product_id__in = product_ids)

        context['order'] = order

        return context
    




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

           order = Order.objects.filter(Q(order_date__gte = start) & Q (order_date__lte = end)).filter(product_id__in = product_ids)        
           
       else:
           order = Order.objects.all().filter(product_id__in = product_ids)


       
       #pdf
       if 'excel' not in request.GET:


                buffer = BytesIO()
            
                # Create the PDF object
                pdf = SimpleDocTemplate(buffer, pagesize=letter)

                #  data for the table
                data = []
                header = ["Order Date", "Order ID", "Category", "Brand", "Sales Amount"]
                data.append(header)

                for report in order:
                    data.append([str(report.order_date.date()), str(report.id), report.product_id.category.category_name, report.product_id.brand.brand_name, str(report.amount)])

                # Creating  the table
                table = Table(data, colWidths=[100, 100, 100, 100, 100], rowHeights=10*len(data))

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



class salesreport_filter(View):

    def post(self,request):

        start_str = request.POST['from']
        end_str = request.POST['to']

        start =  datetime.strptime(start_str, '%Y-%m-%d').date()
        end =  datetime.strptime(end_str, '%Y-%m-%d').date()
        try:
          order = Order.objects.filter(Q(order_date__gte = start) & Q (order_date__lte = end))
          return render(request,'vendor_salesreport.html',{'order':order,'start':start_str,'end':end_str})
        except Exception as e:
            print(e)
            messages.warning(request,'Try with proper values')
            return redirect('vendor_sales_report')
       
    



@login_required(login_url='/vendor-signin')
def logout(request):
    auth.logout(request)
    return redirect('vendor-signin')