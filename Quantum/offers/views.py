from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import View,TemplateView
from .models import Offer
from vendor.models import Product,Variant
from user.models import users
from admin_app.models import Brand
from datetime import datetime


# Create your views here.


class vendor_offers(TemplateView):
    template_name = 'vendor_offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vendor = self.request.user.id

        offer = Offer.objects.filter(vendor_id = vendor)
        context['offer'] = offer

        product =Product.objects.filter(vendor_name = vendor)
        brand1 = [i.brand.brand_name for i in product]
        #to avoid duplicate values
        brand = list(set(brand1))
        context['brand'] = brand

        return context
    




class manage_offer(View):

    def post(self,request):
     
     if self.request.GET.get('id') == None:
        offer_name = self.request.POST['name']
        brand = self.request.POST['brand']
        discount = self.request.POST['percentage']
        expiry = self.request.POST['expiry']
        # vendor_id = users.objects.filter(id =)
        try:
         brand = Brand.objects.get(brand_name = brand)

        except Exception as e:
           print(e)
           messages.warning(request,'Try again with proper values')
           return redirect('vendor_offers')

        offer = Offer.objects.create(
            offer_name = offer_name,
            vendor_id = self.request.user,
            brand = brand,
            percent = discount,
            expiry_date = expiry

        )
        
        products = Product.objects.filter(brand = offer.brand)

        product_ids = [product.id for product in products]

        variant = Variant.objects.filter(Product__id__in=product_ids)

        for i in variant:
           i.final_price -= (float(i.final_price) * float(offer.percent))/100
           i.save()

        

        messages.success(request,'Offer added successfully')

        return redirect('vendor_offers')
    


     else:
            
        offer_name = self.request.POST['name']
        brand = self.request.POST['brand']
        discount = self.request.POST['percentage']
        expiry = self.request.POST['expiry']
        id = self.request.GET.get('id')


        try:
         brand = Brand.objects.get(brand_name = brand)
        except Exception as e:
           print(e)
           messages.warning(request,'Try again with proper values')
           return redirect('vendor_offers')

        offer =  Offer(
            id = id,
            offer_name = offer_name,
            vendor_id = self.request.user,
            brand = brand,
            percent = discount,
            expiry_date = self.request.POST['expiry']


         )

        offer.save()

        products = Product.objects.filter(brand = offer.brand)

        product_ids = [product.id for product in products]

        variant = Variant.objects.filter(Product__id__in=product_ids)

        for i in variant:
           i.final_price += (float(i.final_price) * float(offer.percent))/100
           i.save()
       
       

        messages.success(request,'Successfully updated the offer')
        return redirect('vendor_offers')
     


     
class Changeoffer_status(View):

        def get(self,request):

            action = self.request.GET.get('action')
            id = self.request.GET.get('id')
            offer = Offer.objects.get(id = id)

            if action == 'activate':
               offer.active = True
               offer.save()
               products = Product.objects.filter(brand = offer.brand)

               product_ids = [product.id for product in products]

               variant = Variant.objects.filter(Product__id__in=product_ids)

               for i in variant:
                  i.final_price -= (float(i.final_price) * float(offer.percent))/100
                  i.save()
               
               messages.success(request,'Successfully activated the offer')
               return redirect('vendor_offers')
            
            elif action == 'deactivate':
               
               offer.active = False
               offer.save()

               products = Product.objects.filter(brand = offer.brand)

               product_ids = [product.id for product in products]

               variant = Variant.objects.filter(Product__id__in=product_ids)

               for i in variant:
                  i.final_price += (float(i.final_price) * float(offer.percent))/100
                  i.save()
       



               messages.success(request,'Successfully deactivated the offer')
               return redirect('vendor_offers')

               
               
               
       

            messages.success(request,'Successfully deleted the offer')
            return redirect('vendor_offers')
     

     