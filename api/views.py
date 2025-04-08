from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product, Category
from .serializers import CategorySerializer, ProductSerializer, RegisterSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from accounts.models import Account

# دالة إرسال الإيميل
def send_verification_email(email, activation_link):
    subject = 'Activate your account'
    body = f'Click the link to activate your account: {activation_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    email_msg = EmailMessage(subject=subject, body=body, from_email=from_email, to=[email])
    email_msg.send()

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

        send_verification_email(user.email, activation_link)

        return Response({'message': 'User registered successfully. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        return Response({'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)

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

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def product_api(request, slug=None):
    if request.method == 'GET':
        if slug:
            product = get_object_or_404(Product, slug=slug, status=Product.Status.AVAILABLE)
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
