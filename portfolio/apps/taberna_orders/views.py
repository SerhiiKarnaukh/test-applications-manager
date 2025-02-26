import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.models import PayPalIPN

from .models import Order, Payment, OrderProduct
from taberna_cart.models import CartItem

from .forms import OrderForm

from .utils import (create_order_from_form, generate_order_number, create_payment,
                    update_order, create_order_products, clear_cart, send_order_email)
from taberna_cart.utils import calculate_cart_totals

stripe.api_key = settings.STRIPE_PRIVATE_KEY


def place_order(request):
    user_profile = request.user.userprofile

    cart_items = CartItem.objects.filter(user=user_profile)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('store')

    total, quantity, tax, grand_total = calculate_cart_totals(cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        scheme = "https" if settings.DEBUG is False else request.scheme
        host = request.get_host()
        if form.is_valid():
            order = create_order_from_form(form, user_profile, grand_total, tax, request)
            order.order_number = generate_order_number(order)
            order.save()

            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": grand_total,
                "item_name": "Ordering Taberna store products",
                'no_shipping': '2',
                "invoice": order.order_number,
                "currency_code": "USD",
                "notify_url": f"{scheme}://{host}{reverse('paypal-ipn')}",
                "return_url": f"{scheme}://{host}{reverse('order_complete', kwargs={'order_number':order.order_number})}",
                "cancel_return": f"{scheme}://{host}{reverse('order_failed')}",
            }

            paypal_form = PayPalPaymentsForm(initial=paypal_dict)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'quantity': quantity,
                'tax': tax,
                'grand_total': grand_total,
                'paypal': paypal_form
            }
            return render(request, 'taberna_orders/payments.html', context)
        else:
            messages.error(request, "Invalid form data!")
            return redirect('checkout')
    return redirect('checkout')


def order_complete(request, order_number):
    import time

    time.sleep(10)

    try:
        ipn = get_object_or_404(PayPalIPN, invoice=order_number)
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=ipn.txn_id)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'taberna_orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def order_failed(request):

    return render(request, 'taberna_orders/order_failed.html')


@require_POST
@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, endpoint_secret
        )
    except stripe.error.StripeError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        stripe_session_id = session.get('id')
        order = get_object_or_404(Order, stripe_checkout_session_id=stripe_session_id)

        if order.is_ordered:
            return HttpResponse(status=400)

        payment = create_payment(order.user, order.id, 'Stripe', order.order_total, 'Completed')
        update_order(order, payment)
        create_order_products(order, payment, order.user)
        clear_cart(order.user)
        send_order_email(order)

    return HttpResponse(status=200)
