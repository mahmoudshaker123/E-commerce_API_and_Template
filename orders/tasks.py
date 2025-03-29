from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from .models import Order
from django.conf import settings
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO


@shared_task
def send_emails(order_id):
    order = Order.objects.get(order_id=order_id)
    subject = f'Order number {order.order_id}'
    message = f'Dear {order.get_full_name()},\n\n' \
              f'You have successfully placed an order. Your order ID is {order.order_id}.'
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent


@shared_task
def payment_complated(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - Invoice for Order {order.order_id}'
    message = f'Dear {order.get_full_name()},\n\n' \
              f'You have successfully bought an order. Your order ID is {order.order_id}.'

    # توليد PDF للفاتورة
    html = render_to_string('orders/pdf.html', {'order': order})
    pdf_file = BytesIO()
    weasyprint.HTML(string=html).write_pdf(pdf_file)

    # إرسال الإيميل مع الفاتورة كمرفق
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])
    email.attach(f'order_{order.order_id}.pdf', pdf_file.getvalue(), 'application/pdf')
    email.send()
