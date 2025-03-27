from django.shortcuts import render
from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    success = False  # تعريف success بقيمة افتراضية في بداية الدالة

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, 
                    product=item['product'],  
                    price=item['price'],  
                    quantity=item['quantity']
                )
            # تفريغ السلة بعد الطلب
            cart.clear()
            success = True
            return render(request, 'orders/created.html', {'order': order, 'success': success})
    else:
        form = OrderForm()

    return render(request, 'orders/created.html', {'cart': cart, 'form': form, 'success': success})
