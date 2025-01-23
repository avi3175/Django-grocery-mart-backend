from rest_framework import serializers
from .models import Cart, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product_name', 'quantity', 'price', 'total_price', 'created_at']




from rest_framework import serializers
from .models import Cart, Order

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)  # Add product name as a custom field

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_name', 'quantity', 'total_price', 'created_at', 'updated_at']
