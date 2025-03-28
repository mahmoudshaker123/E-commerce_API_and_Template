from django.shortcuts import render
from .models import Order, OrderItem
from .forms import OrderForm , OrderPaymentForm
from cart.cart import Cart
from django.core.mail import send_mail 
from django.conf import settings
from .tasks import send_emails

def order_create(request):
    cart = Cart(request)
    success = False  

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

            # ارسال ايميل بالطلب
            order_id = order.order_id
            send_emails.delay(order_id)

            success = True

            return render(request, 'orders/created.html', {'order': order, 'success': success})
    else:
        form = OrderForm()

    return render(request, 'orders/created.html', {'cart': cart, 'form': form, 'success': success})


def order_payment(request, order_id):
    pass