from django.shortcuts import render
from random import choice

from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

from . models import Donation


def my_donation(request):
    scheme = "https" if settings.DEBUG is False else request.scheme
    host = request.get_host()

    try:
        donation = choice(Donation.objects.all())
    except IndexError:
        donation = type('Donation', (), {"amount": 10, "title": "Default Donation"})

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": donation.amount,
        "item_name": donation.title,
        'no_shipping': '2',
        "invoice": str(uuid.uuid4()),
        "currency_code": "USD",
        "notify_url": f"{scheme}://{host}{reverse('paypal-ipn')}",
        "return_url": f"{scheme}://{host}{reverse('payment-success')}",
        "cancel_return": f"{scheme}://{host}{reverse('payment-failed')}",
    }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'donation/includes/my-donation.html', {'paypal_form': paypal_form})


def payment_success(request):
    import time

    time.sleep(10)

    return render(request, 'donation/includes/payment-success.html')


def payment_failed(request):

    return render(request, 'donation/includes/payment-failed.html')
