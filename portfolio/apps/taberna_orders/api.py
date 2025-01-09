from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from taberna_cart.models import CartItem

from .forms import OrderForm

from .utils import (create_order_from_form, generate_order_number, create_payment,
                    update_order, create_order_products, clear_cart, send_order_email)
from taberna_cart.utils import calculate_cart_totals


class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        cart_items = CartItem.objects.filter(user=user_profile)

        if not cart_items.exists():
            return Response({"error": "Your cart is empty!"}, status=status.HTTP_400_BAD_REQUEST)

        total, quantity, tax, grand_total = calculate_cart_totals(cart_items)

        form = OrderForm(request.data)
        if form.is_valid():
            order = create_order_from_form(form, user_profile, grand_total, tax, request)
            order.order_number = generate_order_number(order)
            order.save()

            try:
                with transaction.atomic():
                    payment = create_payment(order.user, order.id, 'Stripe', order.order_total, 'Completed')
                    update_order(order, payment)
                    create_order_products(order, payment, order.user)
                    clear_cart(order.user)
                    send_order_email(order)
            except Exception as e:
                print(f"Error processing payment: {e}")

            return Response({
                "order": {
                    "id": order.id,
                    "order_number": order.order_number,
                    "grand_total": grand_total,
                    "tax": tax,
                    "status": order.status,
                    'total': total,
                    'quantity': quantity,
                },
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)
