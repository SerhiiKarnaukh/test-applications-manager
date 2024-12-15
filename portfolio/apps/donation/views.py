from django.shortcuts import render


def my_donation(request):

    return render(request, 'donation/includes/my-donation.html')


def payment_success(request):

    return render(request, 'donation/includes/payment-success.html')


def payment_failed(request):

    return render(request, 'donation/includes/payment-failed.html')
