from django.shortcuts import render,redirect
from user.models import users
from django.contrib import auth
from django.contrib import messages
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from.models import *
import datetime
# Create your views here.
@never_cache
@login_required(login_url='/admin')
def admin_pannel(request):
    return render(request,'admin_pannel.html')


#----------------------------------------------------------------- user management------------------------------------------------------------------------------------------------------
@login_required(login_url='/admin')
def user_management(request):
    user = {
        'user': users.objects.filter(is_staff = False)
    }
    
    return render(request,'user_management.html',user)

def user_delete(request,id):
    usr = users.objects.filter(id = id).delete()
    return redirect('admin_users')

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------- vendor management--------------------------------------------------------------------------------------------------------

@login_required(login_url='/admin')
def vendor_management(request):
    vendor ={
        'vendor': users.objects.filter( Q(is_staff = True) & Q(is_superadmin = False))
    }

    return render(request,'vendor_management.html',vendor)

def vendor_delete(request,id):
    users.objects.filter(id = id).delete()
    return redirect('admin_vendors')

def block(request,id):
    users.objects.filter(id = id).update(is_active = False) 
    messages.success(request,'blocked successfuly')

    if users.objects.filter(id = id).filter(is_staff = True):
        return redirect('admin_vendors')
    else:
        return redirect('admin_users')
    

def unblock(request,id):
    users.objects.filter(id = id).update(is_active = True)
    messages.success(request,'unblocked successfuly')

    if users.objects.filter(id = id).filter(is_staff = True):
        return redirect('admin_vendors')
    else:
        return redirect('admin_users')
    


    

#------------------------------------------------------------------------------------------Category and Brand ------------------------------------------------------------------------------------------------
# ===================================Categories=======================================================

@login_required(login_url='/admin')
def category_management(request):

   context =  { 'category':Category.objects.all(),

     }
  
   return render(request,'category_management.html',context)


@login_required(login_url='/admin')
def add_category(request):

    if request.method == 'POST':
        try:
          category_logo = request.FILES['logo']
          category_name = request.POST['category_name']
          commission = request.POST['commission']
        except:
            messages.warning(request,'Image  can\'t be empty')
            return redirect('admin_category')
            
        if   category_name == '':
            messages.warning(request,'Category name cant be empty')
            return redirect('admin_category')

        if Category.objects.filter(category_name__icontains = category_name).exists():
               messages.warning(request,'Category already exists')
               return redirect('add_category')
    try:
        category = Category(
              category_image = category_logo,
              category_name = category_name,
              commission = commission
              )

        category.save()

        messages.success(request,'Category added successfully.')
        return redirect('admin_category')
    except:
        messages.warning(request,'Check the details given by you and try agin with proper values.')
        print('check 6')
        return redirect('admin_category')




@login_required(login_url='/admin')
def edit_category(request,id):
    if request.method == 'POST':

        try:
          category_logo = request.FILES['logo']
          category_name = request.POST['category_name']
          commission = request.POST['commission']

        except:
            messages.warning(request,'Image or name can\'t be empty')
            return redirect('admin_category')


        if   category_name == '':
            messages.warning(request,'Category name cant be empty')
            return redirect('admin_category')   

        
        try:
         category = Category(
                id=id,
                category_image = category_logo,
                category_name = category_name,
                commission = commission,
                date_added = datetime.datetime.now(),
                last_update = datetime.datetime.now()
            )

         category.save()


         messages.success(request,'Category Updated successfully')
         return redirect('admin_category')
        except:
            messages.warning(request,'check your credentials and try again')
            return redirect('admin_category')




@login_required(login_url='/admin')
def delete_category(request,id):
    
           Category.objects.filter(id=id).delete()
           messages.success(request,'Category deleted successfully')
           return redirect('admin_category')



# =====================================Brands==================================================
@login_required(login_url='/admin')
def brand_management(request):
    context = {
        'brand':Brand.objects.all()
    }
    return render(request,'Brands.html',context)


@login_required(login_url='/admin')
def add_brand(request):
    if request.method == 'POST':

        try:
          brand_logo = request.FILES['logo']
          brand_name = request.POST['brand_name']

        except:
            messages.warning(request,'Image can\'t be empty')
            return redirect('admin_brand')


        if   brand_name == '':
            messages.warning(request,'Brand name cant be empty')
            return redirect('admin_brand')   

        if Brand.objects.filter(brand_name__icontains = brand_name).exists():
            messages.warning(request,'Brand already exists')
            return redirect('admin_brand')
        else:

            brand = Brand(
                brand_logo = brand_logo,
                brand_name = brand_name
            )

            brand.save()


            messages.success(request,'Brand added successfully')
            return redirect('admin_brand')




@login_required(login_url='/admin')
def edit_brand(request,id):
    if request.method == 'POST':

        try:
          brand_logo = request.FILES['logo']
          brand_name = request.POST['brand_name']

        except:
            messages.warning(request,'Image or name can\'t be empty')
            return redirect('admin_brand')


        if   brand_name == '':
            messages.warning(request,'Brand name cant be empty')
            return redirect('admin_brand')   

        else:

            brand = Brand(
                id=id,
                brand_logo = brand_logo,
                brand_name = brand_name,
                date_added = datetime.datetime.now(),
                last_update = datetime.datetime.now()
            )

            brand.save()


            messages.success(request,'Brand Updated successfully')
            return redirect('admin_brand')





@login_required(login_url='/admin')
def delete_brand(request,id):
        Brand.objects.filter(id=id).delete()
        messages.success(request,'Brand deleted successfully')
        return redirect('admin_brand')





# =============================================================================================================================================================================================

@login_required(login_url='/admin')
def sales_report(request):
    return render(request,'salesreport.html')


# ========================================================================Banner================================================================================================================

@login_required(login_url='/admin')
def banner(request):
    banner = {
        'banner':Banner.objects.all()
    }
    print(banner,'jhgfds')
    return render(request,'banner.html',banner)



@login_required(login_url='/admin')
def add_banner(request):
    if request.method == 'POST':

        try:
            banner_image = request.FILES['bannerimage']
            banner_title = request.POST['bannertitle']
            banner_description = request.POST['bannerdescription']
        except:
            messages.warning(request,'please fill  the columns')

        if Banner.objects.filter(banner_title = banner_title):
            messages.warning(request,'A banner with the title already exists.')
            return redirect('admin_banners')

            
        try:
                banner = Banner(
                    banner_image = banner_image,
                    banner_title = banner_title,
                    banner_description = banner_description
                )

                banner.save()
                return redirect("admin_banners")
            
        except:
                messages.warning(request,'Something went Wrong')
                return redirect('admin_banners')
            


        
    return redirect(request,'banner.html')

@login_required(login_url='/admin')
def edit_banner(request,id):
    if request.method == 'POST':

        try:
            banner_image = request.FILES['bannerimage']
            banner_title = request.POST['bannertitle']
            banner_description = request.POST['bannerdescription']
        except:
            messages.warning(request,'please fill  the columns')

            
        try:
                banner = Banner(
                    id = id,
                    banner_image = banner_image,
                    banner_title = banner_title,
                    banner_description = banner_description
                )

                banner.save()
                return redirect('admin_banners')
            
        except:
                messages.warning(request,'Something went Wrong')
                return redirect('admin_banners')

    return render(request,'banner.html')

@login_required(login_url='/admin')
def delete_banner(request,id):

    Banner.objects.filter(id = id).delete()
    messages.success(request,'Banner Deleted')
    return redirect('admin_banners')

    
# ========================================================================================================================================================================================

@never_cache
def admin_signin(request):
    if request.user.is_authenticated and request.user.is_superadmin ==True:
        return redirect('admin_pannel')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        admin = auth.authenticate(email = email, password = password)

        if admin is not None and admin.is_superadmin:
            auth.login(request,admin)
            return redirect('admin_pannel')
        else:
            messages.warning(request,'Password or Email is invalid.Try again')
            return redirect('admin_signin')


    return render(request,'admin_signin.html')

login_required(login_url='/admin')
def logout(request):
    auth.logout(request)
    return redirect('admin')
