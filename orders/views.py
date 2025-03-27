from django.shortcuts import render
from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import Cart
from django.core.mail import send_mail 
from django.conf import settings


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
            # ارسال بريد الكتروني

            subject = 'Order {}'.format(order.order_id)
            message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name, order.order_id)
            for item in cart:
                product_name = item['product'].name
                message += '\n\nProduct: {}\nPrice: {}\nQuantity: {}\n'.format(product_name, item['price'], item['quantity'])
            
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data['email']]
            send_mail(subject, message, email_from, recipient_list)
            success = True

            return render(request, 'orders/created.html', {'order': order, 'success': success})
    else:
        form = OrderForm()

    return render(request, 'orders/created.html', {'cart': cart, 'form': form, 'success': success})
