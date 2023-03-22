from rest_framework import generics
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Product, Category, ReviewRating, ProductGallery
from .serializers import ProductSerializer
from cart.models import CartItem
from cart.views import _get_cart_id
from .forms import ReviewForm
from orders.models import OrderProduct


# for Django Template Language
class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def create_store_data(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            try:
                order_product = OrderProduct.objects.filter(
                    user=self.request.user,
                    product__slug=self.kwargs['slug']).exists()
            except OrderProduct.DoesNotExist:
                order_product = None
        else:
            order_product = None
            context['orderproduct'] = order_product
        context['product_gallery'] = ProductGallery.objects.filter(
            product__slug=self.kwargs['slug'])
        context['reviews'] = ReviewRating.objects.filter(
            product__slug=self.kwargs['slug'], status=True)
        context['in_cart'] = CartItem.objects.filter(
            cart__cart_id=_get_cart_id(self.request),
            product__slug=self.kwargs['slug']).exists()
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.create_store_data()
        return dict(list(context.items()) + list(c_def.items()))


class CategoryDetail(ListView):
    paginate_by = 4
    model = Product
    template_name = 'product/store.html'
    context_object_name = 'products'
    allow_empty = False

    def create_store_data(self, **kwargs):
        context = kwargs
        if 'slug' in self.kwargs:
            context['store_title'] = Category.objects.get(
                slug=self.kwargs['slug'])
            context['product_count'] = Product.objects.filter(
                category__slug=self.kwargs['slug'], is_available=True).count()
            return context
        else:
            context['store_title'] = 'All products'
            context['product_count'] = Product.objects.all().filter(
                is_available=True).count()
            return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.create_store_data()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self, **kwargs):
        if 'slug' in self.kwargs:
            return Product.objects.filter(
                category__slug=self.kwargs['slug'],
                is_available=True).select_related('category')
        else:
            return Product.objects.all().filter(
                is_available=True).select_related('category')


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-date_added').filter(
                Q(description__icontains=keyword)
                | Q(name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'product/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,
                                               product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request,
                             'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,
                                 'Thank you! Your review has been submitted.')
                return redirect(url)


# for Django Rest Framework
class LatestProductsList(generics.ListAPIView):
    queryset = Product.objects.all().filter(is_available=True)[0:6]
    serializer_class = ProductSerializer


class ProductAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'product_slug'
    lookup_field = 'slug'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer