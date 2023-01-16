from django.shortcuts import render
from.serializers import *
from.models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response





class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        id = self.kwargs['id']
        return Cart.objects.filter(user_id = id)
    

    @action(detail=False, methods=['get'])
    def html_view(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return render(request, 'trial.html', {'data': serializer.data})
    



class Add_CartViewSet(viewsets.ModelViewSet):
    serializer_class = Add_CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        id = self.kwargs['id']
        return Cart_items.objects.filter(cart = id)



class Add_CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = Add_CartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



def trial(request):
    return render(request,'trial.html')