from django.shortcuts import render
from django.views.generic import ListView

from product.models import Product, ReviewRating


class FrontPage(ListView):
    model = Product
    template_name = 'core/frontpage.html'
    context_object_name = 'products'

    def create_store_data(self, **kwargs):
        context = kwargs
        products = Product.objects.all().filter(
            is_available=True).select_related('category')
        reviews = None
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id,
                                                  status=True)
        context['reviews'] = reviews
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.create_store_data()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.all().filter(
            is_available=True).select_related('category')[0:6]


def contact(request):
    return render(request, 'core/contact.html')


def about(request):
    return render(request, 'core/about.html')
