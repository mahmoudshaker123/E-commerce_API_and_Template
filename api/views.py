from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product, Category
from .serializers import CategorySerializer, ProductSerializer


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def category_api(request, slug=None):
    if request.method == 'GET':
        if slug:
            category = get_object_or_404(Category, slug=slug)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Object posted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        category = get_object_or_404(Category, slug=slug)
        partial = request.method == 'PATCH'
        serializer = CategorySerializer(category, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Object updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response({'message': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def product_api(request , slug=None):
    if request.method == 'GET':
        if slug:
            product = get_object_or_404(Product, slug=slug , status=Product.Status.AVAILABLE)   
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Product.objects.filter(status=Product.Status.AVAILABLE)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    elif request.method in ['PUT', 'PATCH']:
        product = get_object_or_404(Product, slug=slug)
        partial = request.method == 'PATCH'
        serializer = ProductSerializer(product, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Object updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        product = get_object_or_404(Product, slug=slug)
        product.delete()
        return Response({'message': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
