# storefront/serializers.py

from rest_framework import serializers
from .models import Product, ShippingRate, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source='image', write_only=True, required=False, allow_blank=True)
    # --- CHANGE END ---

    class Meta:
        model = Product
        # --- CHANGE START ---
        # We explicitly list the fields to include the new `image_url`
        fields = ['id', 'page', 'name', 'description', 'price', 'stock', 'image', 'image_url', 'created_at']
        # The page is determined by the URL, not user input, so it should be read-only.
        # The `image` field is read-only because we now write to it via `image_url`.
        read_only_fields = ('owner', 'page', 'image')


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