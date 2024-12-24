from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.db import transaction
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Order, Payment, OrderProduct
from taberna_cart.models import CartItem


@receiver(valid_ipn_received)
def paypal_taberna_payment_received(sender, **kwargs):
    ipn_obj = sender
    invoice = str(ipn_obj.invoice)
    txn_id = str(ipn_obj.txn_id)

    try:
        order = Order.objects.get(order_number=invoice)
    except Order.DoesNotExist:
        print(f"Order with invoice {invoice} does not exist.")
        return

    if ipn_obj.payment_status != ST_PP_COMPLETED:
        print(f"PayPal payment status not completed: {ipn_obj.payment_status}")
        return

    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        print(f"Invalid receiver email: {ipn_obj.receiver_email}")
        return

    try:
        with transaction.atomic():
            payment = create_payment(order.user, txn_id, order.order_total, ipn_obj.payment_status)
            update_order(order, payment)
            create_order_products(order, payment, order.user)
            clear_cart(order.user)
            send_order_email(order)
    except Exception as e:
        print(f"Error processing payment: {e}")


def create_payment(user, txn_id, amount_paid, status):
    payment = Payment(
        user=user,
        payment_id=txn_id,
        payment_method='PayPal',
        amount_paid=amount_paid,
        status=status,
    )
    payment.save()
    return payment


def update_order(order, payment):
    order.payment = payment
    order.is_ordered = True
    order.save()


def create_order_products(order, payment, user):
    cart_items = CartItem.objects.filter(user=user)
    for item in cart_items:
        order_product = OrderProduct.objects.create(
            order=order,
            payment=payment,
            user=user,
            product=item.product,
            quantity=item.quantity,
            product_price=item.product.price,
            ordered=True,
        )
        order_product.variations.set(item.variations.all())
        order_product.save()

        # Reduce product stock
        product = item.product
        product.stock -= item.quantity
        product.save()


def clear_cart(user):
    CartItem.objects.filter(user=user).delete()


def send_order_email(order):
    user = order.user
    mail_subject = 'Thank you for your order!'
    message = render_to_string('taberna_orders/order_received_email.html', {
        'user': user.user,
        'order': order,
    })
    to_email = user.user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
