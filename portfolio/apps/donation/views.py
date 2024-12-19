from django.shortcuts import render

from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid


def my_donation(request):
    scheme = request.scheme
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": 20,
        "item_name": "Donate to charity",
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

    return render(request, 'donation/includes/payment-success.html')


def payment_failed(request):

    return render(request, 'donation/includes/payment-failed.html')
