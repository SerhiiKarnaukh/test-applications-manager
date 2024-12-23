import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Order, Payment, OrderProduct
from taberna_cart.models import CartItem
from taberna_product.models import Product

from .forms import OrderForm

from .utils import create_order_from_form, generate_order_number
from taberna_cart.utils import calculate_cart_totals


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,
                              is_ordered=False,
                              order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request):
    user_profile = request.user.userprofile

    cart_items = CartItem.objects.filter(user=user_profile)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('store')

    total, quantity, tax, grand_total = calculate_cart_totals(cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = create_order_from_form(form, user_profile, grand_total, tax, request)
            order.order_number = generate_order_number(order)
            order.save()

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'quantity': quantity,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'taberna_orders/payments.html', context)
        else:
            messages.error(request, "Invalid form data!")
            return redirect('checkout')
    return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

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
