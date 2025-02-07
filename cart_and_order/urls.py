from django.urls import path
from .views import (
    CartView,
    OrderView,
    OrderHistoryView,
    create_checkout_session,
    stripe_webhook
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart-item'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/history/', OrderHistoryView.as_view(), name='order-history'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),  # Webhook to capture Stripe events
]
