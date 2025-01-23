from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Cart, Order
from .serializers import CartSerializer, OrderSerializer
from products.models import Product

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
            total_price = product.price * quantity

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity, 'total_price': total_price}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.total_price += total_price
                cart_item.save()

            return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            cart_item = Cart.objects.get(id=pk, user=request.user)
            cart_item.delete()
            return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None):
        try:
            cart_item = Cart.objects.get(id=pk, user=request.user)
            quantity = request.data.get('quantity')

            if quantity is None or quantity <= 0:
                return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

            # Update quantity and total price
            product = cart_item.product
            cart_item.quantity = quantity
            cart_item.total_price = product.price * quantity
            cart_item.save()

            return Response(CartSerializer(cart_item).data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)    


    
# cart_and_order/views.py
from decimal import Decimal

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.total_price for item in cart_items)

        # Loop through cart items and create individual Order entries for each
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.total_price
            )

        # Optionally, clear the cart
        cart_items.delete()

        return Response({"message": "Order placed successfully!"}, status=status.HTTP_201_CREATED)



class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
