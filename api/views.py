from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product , Category
from .serializers import CategorySerializer  , ProductSerializer

# Create your views here.


@api_view(['GET' ,'POST' ,'PUT','PATCH' ,'DELETE'])
def category_api(request , slug=None):
    if request.method == 'GET':
        if slug:
            categories = get_object_or_404(Category , slug=slug)
            serializer  = CategorySerializer(categories , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)

        
    elif request.method =='POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Object Post successfuly'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET' , 'POST'])
def product_api(request):
    if request.method == 'GET':
        products = Product.objects.filter(status=Product.Status.AVAILABLE)
        serializer = ProductSerializer(products , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    elif request.method =='POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    
