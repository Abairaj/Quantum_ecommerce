from django.shortcuts import render,redirect
from user.models import users
from django.contrib import auth
from django.contrib import messages
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
@never_cache
@login_required(login_url='/admin')
def admin_pannel(request):
    return render(request,'admin_pannel.html')


def user_management(request):
    return render(request,'user_management.html')

def vendor_management(request):
    return render(request,'vendor_management.html')

def category_management(request):
    return render(request,'category_management.html')


def sales_report(request):
    return render(request,'salesreport.html')

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
