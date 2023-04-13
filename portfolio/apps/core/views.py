from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


def app_detail(request):
    return render(request, 'core/portfolio_detail.html')
