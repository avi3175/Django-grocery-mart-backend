from django.urls import path
from .views import CartView, OrderView, OrderHistoryView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart-item'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/history/', OrderHistoryView.as_view(), name='order-history'),
]
