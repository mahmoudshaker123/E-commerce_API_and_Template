from django.shortcuts import render , redirect , get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm

# Create your views here.


@require_POST
def cart_add(request , product_id):
    cart = Cart(request)
    product = get_object_or_404(Product , id=product_id , status=Product.Status.AVAILABLE)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product , quantity=cd['quantity'] , update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request , product_id):
    cart = Cart(request)
    product = get_object_or_404(Product , id=product_id , status=Product.Status.AVAILABLE)
    cart.remove(product)
    return redirect('cart:cart_detail') 


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'] , 'update':True})
    context={
        'cart':cart,
        'coupon_apply_form':CouponApplyForm }
    return render(request , 'cart/cart_details.html' , context)



