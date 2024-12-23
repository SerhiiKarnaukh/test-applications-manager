import requests
from django.shortcuts import redirect
from taberna_cart.utils import get_cart_id

from taberna_cart.models import Cart, CartItem


def handle_cart_after_login(request, user_profile):
    """
    Processes the cart after the user logs in.
    """
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return

        # Collecting information about product variations
        product_variations = [list(item.variations.all()) for item in cart_items]

        # Checking a user's existing products
        user_cart_items = CartItem.objects.filter(user=user_profile)
        existing_variations = [list(item.variations.all()) for item in user_cart_items]
        item_ids = [item.id for item in user_cart_items]

        for variation in product_variations:
            if variation in existing_variations:
                # Increasing the number of existing products
                index = existing_variations.index(variation)
                item_id = item_ids[index]
                item = CartItem.objects.get(id=item_id)
                item.quantity += 1
                item.save()
            else:
                # Linking items from the cart to the user
                for item in cart_items:
                    item.user = user_profile
                    item.save()
    except Cart.DoesNotExist:
        pass


def redirect_to_next_or_dashboard(request):
    """
    Performs a redirect to the 'next' parameter or dashboard.
    """
    url = request.META.get('HTTP_REFERER', None)
    if url:
        try:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))
            if 'next' in params:
                return redirect(params['next'])
        except Exception:
            pass
    return redirect('dashboard')
