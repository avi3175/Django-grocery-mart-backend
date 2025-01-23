from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    product_name = models.CharField(max_length=255, null=True, blank=True)  # Make it nullable temporarily
    quantity = models.PositiveIntegerField(null=True, blank=True)  # Make it nullable temporarily
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Make it nullable temporarily
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Make it nullable temporarily
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Make it nullable temporarily

    def __str__(self):
        return f"Order by {self.user.username} on {self.created_at}"
