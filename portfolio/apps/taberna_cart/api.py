from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartItemSerializer
from .utils import prepare_cart_context


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
