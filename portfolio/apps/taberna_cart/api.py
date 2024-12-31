from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CartItem
from taberna_product.models import Product
from taberna_profiles.models import UserProfile

from .serializers import CartItemSerializer
from .utils import prepare_cart_context, get_product_variations, get_or_create_cart, handle_cart_item


class CartAPIView(APIView):

    def get(self, request, *args, **kwargs):
        context = prepare_cart_context(request.user, request)
        serialized_data = {
            'total': context['total'],
            'quantity': context['quantity'],
            'tax': context['tax'],
            'grand_total': context['grand_total'],
            'cart_items': CartItemSerializer(
                context['cart_items'],
                many=True,
                context={"request": request}
            ).data,
        }
        return Response(serialized_data)


class AddToCartView(APIView):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product_variation = get_product_variations(product, request.data)

        if request.user.is_authenticated and UserProfile.objects.filter(user=request.user).exists():
            current_user = UserProfile.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(user=current_user, product=product)
            handle_cart_item(cart_items, product_variation, product, user=current_user)
        else:
            cart = get_or_create_cart(request)
            cart_items = CartItem.objects.filter(cart=cart, product=product)
            handle_cart_item(cart_items, product_variation, product, cart=cart)

        return Response({"message": "Product added to cart successfully"}, status=status.HTTP_200_OK)
