from django.conf import settings
from decimal import Decimal

from .models import Cart, CartItem

from taberna_product.models import Variation
from taberna_profiles.models import UserProfile


def get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def get_product_variations(product, post_data):
    """Getting product variations from POST data."""
    variations = []
    for key, value in post_data.items():
        try:
            variation = Variation.objects.get(
                product=product,
                variation_category__iexact=key,
                variation_value__iexact=value
            )
            variations.append(variation)
        except Variation.DoesNotExist:
            continue
    return variations


def get_or_create_cart(request):
    """Receiving or creating a shopping cart for an unauthenticated user."""
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=get_cart_id(request))
        cart.save()
    return cart


def handle_cart_item(cart_items, product_variation, product, user=None, cart=None):
    """
    Processing adding an item to cart:
    - Increasing the quantity if a variation already exists.
    - Create a new entry if the variation is not found.
    """
    ex_var_list = []
    item_ids = []

    for item in cart_items:
        existing_variations = list(item.variations.all())
        ex_var_list.append(existing_variations)
        item_ids.append(item.id)

    if product_variation in ex_var_list:
        # Increase quantity for an existing item
        index = ex_var_list.index(product_variation)
        item_id = item_ids[index]
        item = CartItem.objects.get(id=item_id)
        item.quantity += 1
        item.save()
    else:
        # Create a new entry
        item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=user,
            cart=cart
        )
        if product_variation:
            item.variations.add(*product_variation)
        item.save()


def get_cart_item(request, product, cart_item_id):
    """
    Helper function to retrieve the cart item for the current user or guest.
    """
    if request.user.is_authenticated and UserProfile.objects.filter(user=request.user).exists():
        current_user = UserProfile.objects.get(user=request.user)
        return CartItem.objects.get(product=product, user=current_user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        return CartItem.objects.get(product=product, cart=cart, id=cart_item_id)


def get_cart_items(user, request):
    """
    Helper function to retrieve ALL cart items for the current user or guest.
    """
    if user.is_authenticated and UserProfile.objects.filter(user=user).exists():
        current_user = UserProfile.objects.get(user=user)
        return CartItem.objects.filter(user=current_user, is_active=True).order_by('-id')
    else:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        return CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')


def calculate_cart_totals(cart_items):
    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    tax_rate = Decimal(getattr(settings, 'TABERNA_TAX_RATE', 0.02))
    tax = round(total * tax_rate, 2)
    grand_total = total + tax
    return total, quantity, tax, grand_total


def prepare_cart_context(user, request):
    """
    Helper function to prepare the context for cart-related views.
    """
    try:
        cart_items = get_cart_items(user, request)
        total, quantity, tax, grand_total = calculate_cart_totals(cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = quantity = tax = grand_total = 0

    return {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
