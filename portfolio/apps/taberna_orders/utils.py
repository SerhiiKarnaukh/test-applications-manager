import stripe
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, Payment, OrderProduct
from taberna_cart.models import CartItem


def create_order_from_form(form, user_profile, grand_total, tax, request):
    """
    Creates an Order object based on a form and additional data.
    """
    order = Order(
        user=user_profile,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        phone=form.cleaned_data['phone'],
        email=form.cleaned_data['email'],
        address_line_1=form.cleaned_data['address_line_1'],
        address_line_2=form.cleaned_data['address_line_2'],
        country=form.cleaned_data['country'],
        state=form.cleaned_data['state'],
        city=form.cleaned_data['city'],
        order_note=form.cleaned_data['order_note'],
        order_total=grand_total,
        tax=tax,
        ip=request.META.get('REMOTE_ADDR'),
    )
    order.save()
    return order


def generate_order_number(order):
    """
    Generates a unique order number.
    """
    current_date = datetime.date.today().strftime("%Y%m%d")
    return f"{current_date}{order.id}"


def create_payment(user, txn_id, payment_method, amount_paid, status):
    payment = Payment(
        user=user,
        payment_id=txn_id,
        payment_method=payment_method,
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


def stripe_charge_create(request, amount, order):
    # https://docs.stripe.com/api/charges/create
    stripe_token = request.data.get('stripe_token')
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    stripe.Charge.create(
        amount=int(amount * 100),
        currency='USD',
        description=f'Order #{order.order_number}',
        source=stripe_token,
        receipt_email=request.user.email
    )
