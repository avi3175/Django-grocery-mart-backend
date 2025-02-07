import stripe
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Cart, Order
from products.models import Product
from .serializers import CartSerializer, OrderSerializer

# Set Stripe API key
stripe.api_key = settings.STRIPE_TEST_API_KEY  

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        total_price = product.price * quantity

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity, "total_price": total_price},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.total_price = cart_item.quantity * product.price
            cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        cart_item_id = request.data.get("cart_item_id")

        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.total_price for item in cart_items)

        try:
            # Create a Stripe PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),  # Convert to cents
                currency="usd",
            )
            
            # Save order details in the database
            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price,
                    payment_intent_id=payment_intent.id  # Store Stripe Payment ID
                )

            cart_items.delete()  # Clear cart after checkout starts

            return Response({"client_secret": payment_intent.client_secret}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        order = Order.objects.filter(payment_intent_id=payment_intent["id"]).first()
        if order:
            order.paid = True
            order.save()

    return HttpResponse(status=200)

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            items = data.get("items", [])
            line_items = []
            orders = []

            for item in items:
                product = Product.objects.get(id=item["id"])
                order = Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=item["quantity"],
                    total_price=item["price"] * item["quantity"]
                )
                orders.append(order)

                line_items.append({
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item["name"]},
                        "unit_amount": int(item["price"] * 100),
                    },
                    "quantity": item["quantity"],
                })

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="http://localhost:5173/success",
                cancel_url="http://localhost:5173/cancel",
            )

            return JsonResponse({"id": checkout_session.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
