from django.shortcuts import render,redirect
from user.models import users
from django.contrib import auth
from django.contrib import messages
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from.models import *

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
    category ={
   'category':Category.objects.all()

    }

    return render(request,'category_management.html',category)

@login_required(login_url='/admin')
def add_category(request):

    if request.method == 'POST':

        category_logo = request.FILES['logo']
        category_name = request.POST['category_name']

    category = Category(
        category_image = category_logo,
        category_name = category_name
    )

    category.save()

    messages.success(request,'Category_added successfully.')
    return redirect('admin_category')


# =====================================Brands==================================================
@login_required(login_url='/admin')
def brand_management(request):
    brands ={
   'brand':Brand.objects.all()

    }

    return render(request,'category_management.html',brands)




# =============================================================================================================================================================================================

@login_required(login_url='/admin')
def sales_report(request):
    return render(request,'salesreport.html')



@login_required(login_url='/admin')
def banner(request):
    return render(request,'banner.html')
    


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
