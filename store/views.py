from django.shortcuts import render , redirect , get_object_or_404
from .models import Product , Category
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from cart.forms import CartAddProductForm
from django.core.cache import cache
from django.core.paginator import Paginator
# Create your views here.

def list_product(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(status=Product.Status.AVAILABLE)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  

    context = {
        'products': page_obj,  
        'category': category,
        'categories': categories,
        'page_obj': page_obj,  
    }
    return render(request, 'store/list_product.html', context)

def product_detail(request, product_slug):
    cache_key = f'product_{product_slug}' 
    product = cache.get(cache_key)
    if not product:
        product = get_object_or_404(Product, slug=product_slug , status=Product.Status.AVAILABLE)
        cache.set(cache_key, product , timeout=60*30)
        

    product = get_object_or_404(Product, slug=product_slug , status=Product.Status.AVAILABLE)
    cart_product_form = CartAddProductForm()
    context = {
        'detail':product,
        'cart_product_form':cart_product_form,
    }
    return render(request , 'store/product_detail.html' , context)

  
def product_search(request):
    query = request.GET.get('query', None)
    results = []

    if query:
        search_query = SearchQuery(query)
        results = Product.objects.annotate(
            search=SearchVector('name', 'description')
        ).filter(search=search_query, status=Product.Status.AVAILABLE)

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'store/search.html', context)

