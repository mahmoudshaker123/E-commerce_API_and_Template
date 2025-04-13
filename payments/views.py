from django.shortcuts import render
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get("order_id")
            if not order_id:
                return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.get(order_id=order_id)
            total_amount = int(order.get_total_cost() * 100)  

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Order {order.order_id}",
                            },
                            "unit_amount": total_amount,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=settings.SITE_URL + "/payment-success",
                cancel_url=settings.SITE_URL + "/payment-cancel",
                metadata={
                    "order_id": order.order_id,
                },
            )

            return Response({"checkout_url": session.url})
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=endpoint_secret
            )
        except ValueError as e:
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=400)

        # Handle successful payment
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session["metadata"].get("order_id")

            try:
                order = Order.objects.get(order_id=order_id)
                order.paid = True
                order.save()
            except Order.DoesNotExist:
                pass

        return Response(status=200)