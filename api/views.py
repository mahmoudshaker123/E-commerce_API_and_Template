from email.message import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product, Category
from .serializers import CategorySerializer, ProductSerializer, RegisterSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail as django_send_mail
from django.conf import settings

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

@api_view(['POST'])
def register_api(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False 
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = request.get_host()
        activation_link = f"http://{current_site}/api/activate/{uid}/{token}/"

        send_verification_email(user, activation_link)

        return Response({'message': 'User registered successfully. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_verification_email(user, activation_link):
    email_subject = 'Activate your account'
    email_body = f'Click the link to activate your account: {activation_link}'
    
    django_send_mail(
        subject=email_subject,
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,  
         
    )
