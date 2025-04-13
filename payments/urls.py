from django.urls import path
from .views import CreateStripeCheckoutSessionView, StripeWebhookView

urlpatterns = [
    path('create-checkout-session/', CreateStripeCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
