from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from .models import Cart, CartItem

from taberna_product.models import Product
from taberna_profiles.models import UserProfile

from .utils import (get_product_variations, get_or_create_cart, handle_cart_item,
                    get_cart_item, prepare_cart_context)


def cart(request):
    context = prepare_cart_context(request.user, request)
    return render(request, 'taberna_cart/cart.html', context)


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = get_product_variations(product, request.POST)

    if request.user.is_authenticated and UserProfile.objects.filter(user=request.user).exists():
        current_user = UserProfile.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(user=current_user, product=product)
        handle_cart_item(cart_items, product_variation, product, user=current_user)
    else:
        cart = get_or_create_cart(request)
        cart_items = CartItem.objects.filter(cart=cart, product=product)
        handle_cart_item(cart_items, product_variation, product, cart=cart)

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = get_cart_item(request, product, cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        # Optionally log the error or show a message
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = get_cart_item(request, product, cart_item_id)
        cart_item.delete()
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        # Optionally log the error or show a message
        pass
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    context = prepare_cart_context(request.user, request)
    return render(request, 'taberna_cart/checkout.html', context)
