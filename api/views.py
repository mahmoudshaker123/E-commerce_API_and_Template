from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product , Category
from .serializers import CategorySerializer  , ProductSerializer

# Create your views here.


@api_view(['GET'])
def category_api(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer  = CategorySerializer(categories , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
def product_api(request):
    if request.method == 'GET':
        products = Product.objects.filter(status=Product.Status.AVAILABLE)
        serializer = ProductSerializer(products , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
