from django.urls import path
from .views import cart, add_cart, checkout, remove_cart, remove_cart_item

from . import api

urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',
         remove_cart,
         name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',
         remove_cart_item,
         name='remove_cart_item'),
    path('checkout/', checkout, name='checkout'),

    # API
    path('api/cart/', api.CartAPIView.as_view(), name='taberna-api-cart'),
]
