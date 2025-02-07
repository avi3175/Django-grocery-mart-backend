from rest_framework import serializers
from .models import Cart, Order

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_name', 'quantity', 'total_price', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_name', 'quantity', 'total_price', 'paid', 'created_at']
