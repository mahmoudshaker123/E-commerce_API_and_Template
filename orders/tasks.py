from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


@shared_task
def send_emails(order_id):

    order = Order.objects.get(order_id=order_id)
    subject = f'Order number {order.order_id}'
    message = f'Dear {order.get_full_name()},\n\n' \
              f'You have successfully placed an order. Your order ID is {order.order_id}.'
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent