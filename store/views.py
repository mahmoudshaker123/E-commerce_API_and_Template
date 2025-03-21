from django.shortcuts import render , redirect
from .models import Product , Category
# Create your views here.

def list_product(request):
    product = Product.objects.filter(status =Product.Status.AVAILABLE)
    context={
        'product':product
    }
    return render(request , 'store/list_product.html' , context)
