from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/cart_and_order/', include('cart_and_order.urls')),
    path('api/comments/', include('comments.urls')),
]
