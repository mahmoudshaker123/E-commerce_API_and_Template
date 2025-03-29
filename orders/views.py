from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404 ,redirect
from .models import Order, OrderItem
from .forms import OrderForm , OrderPaymentForm
from cart.cart import Cart
from django.core.mail import send_mail 
from django.conf import settings
from .tasks import send_emails
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import os
import weasyprint





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
            return redirect('orders:payment_order', order_id=order.id)

            return render(request, 'orders/created.html', {'order': order, 'success': success})
    else:
        form = OrderForm()

    return render(request, 'orders/created.html', {'cart': cart, 'form': form, 'success': success})


def order_payment_by_vodafone(request, order_id):
    order = get_object_or_404(Order , id=order_id)
    if request.method == 'POST':
        form = OrderPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            order_payment = form.save(commit=False)
            order_payment.order = order
            order_payment.paid = True  # تعيين حالة الدفع
            order_payment.save()
            return redirect('orders:payment_success', order_id=order.id)
    else:
        form = OrderPaymentForm()

    return render(request, 'orders/payment.html', {'form': form, 'order': order})

    
def payment_success(request, order_id):
    order= get_object_or_404(Order, id=order_id)
    return render(request, 'orders/payment_success.html', {'order': order})


@staff_member_required
def admin_order_pdf(request , order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.order_id}.pdf' 
    weasyprint.HTML(string=html).write_pdf(response)
    return response

    