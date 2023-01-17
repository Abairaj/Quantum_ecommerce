from django.shortcuts import render
from.serializers import *
from rest_framework.views import APIView

# Create your views here.



class OrderAPI_View(APIView):
    
    def get(self,request):
        pass