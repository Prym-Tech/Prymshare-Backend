# storefront/serializers.py

from rest_framework import serializers
from .models import Product, ShippingRate, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Include all fields from the model
        fields = '__all__'
        # Set 'owner' as read-only because it's determined by the request user, not client input
        read_only_fields = ('owner',)



class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_email', 'customer_address', 'total_amount', 'payment_status', 'created_at', 'items']