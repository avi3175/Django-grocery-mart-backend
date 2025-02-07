from django.contrib import admin
from .models import Cart, Order

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price', 'created_at']
    search_fields = ['user__username', 'product__name']
    list_filter = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_product_name', 'quantity', 'total_price', 'paid', 'created_at']
    search_fields = ['user__username', 'product_name']
    list_filter = ['paid', 'created_at']
    readonly_fields = ['payment_intent_id']  # Protects payment data from manual edits

    def get_product_name(self, obj):
        return obj.product_name  # This ensures product_name is displayed correctly
    
    get_product_name.short_description = 'Product Name'  # Sets column title in admin panel
