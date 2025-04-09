from rest_framework import serializers
from .models import Order, OrderItem
from store.models import Product ,Category


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [ 'first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city'] 