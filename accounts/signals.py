from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from django.core.mail import send_mail
from django.conf import settings



@receiver(post_save, sender=Account)
def send_welcome_email(sender, instance, created, **kwargs):
    if created :
        subject = "مرحبًا بك في موقعنا!"
        message = f"مرحبًا {instance.username}، شكرًا لتسجيلك في موقعنا! نتمنى لك تجربة رائعة."
        from_email = settings.DEFAULT_FROM_EMAIL
        user_email = [instance.email]

        send_mail(subject, message, from_email, user_email)