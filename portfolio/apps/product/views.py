from rest_framework import generics, status
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from django.db.models import Q
from django.http import Http404
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .permissions import IsOwnerOrReadOnly
from django.db.models import Count

from .models import Product, Category, ReviewRating, ProductGallery
from .serializers import ProductSerializer, CategorySerializer, AllCategoriesSerializer
from cart.models import CartItem
from cart.views import _get_cart_id
from .forms import ReviewForm
from orders.models import OrderProduct
from django.core.paginator import Paginator


# for Django Template Language
class FrontPage(ListView):
    model = Product
    template_name = 'store/frontpage.html'
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
    return render(request, 'store/contact.html')


def about(request):
    return render(request, 'store/about.html')


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        category = product.category
        context['related_products'] = Product.objects.filter(
            category=category).exclude(id=product.id)
        context['in_cart'] = CartItem.objects.filter(
            cart__cart_id=_get_cart_id(self.request),
            product__slug=product.slug).exists()
        context['reviews'] = ReviewRating.objects.filter(
            product__slug=product.slug, status=True)
        context['order_product'] = None
        if self.request.user.is_authenticated:
            try:
                order_product = OrderProduct.objects.get(
                    user=self.request.user, product=product)
                context['order_product'] = order_product
            except OrderProduct.DoesNotExist:
                pass

        all_gallery_images = ProductGallery.objects.filter(product=product)
        gallery_paginator = Paginator(all_gallery_images, 3)
        all_gallery_images_list = []
        for page in gallery_paginator.page_range:
            current_page = gallery_paginator.get_page(page)
            all_gallery_images_list.append(current_page.object_list)
        context['product_gallery'] = all_gallery_images_list

        return context


class CategoryDetail(ListView):
    paginate_by = 6
    model = Product
    template_name = 'product/store.html'
    context_object_name = 'products'
    allow_empty = False

    def create_store_data(self, **kwargs):
        context = kwargs
        if 'slug' in self.kwargs:
            context['store_title'] = str(
                Category.objects.get(slug=self.kwargs['slug']))
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


class ProductSearchListView(ListView):
    model = Product
    template_name = 'product/store.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('keyword')
        if query:
            return Product.objects.filter(
                Q(description__icontains=query)
                | Q(name__icontains=query)).order_by('-date_added')
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        context['store_title'] = 'Search Result'
        return context


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
class LatestProductsAPIList(generics.ListAPIView):
    queryset = Product.objects.all().filter(is_available=True)[0:6]
    serializer_class = ProductSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class ProductAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'product_slug'
    lookup_field = 'slug'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# class CategoryAPIDetail(APIView):

#     def get_object(self, category_slug):
#         try:
#             return Category.objects.get(slug=category_slug)
#         except Category.DoesNotExist:
#             raise Http404

#     def get(self, request, category_slug, format=None):
#         category = self.get_object(category_slug)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)


class CategoryAPIDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({'error': 'Category not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering based on the slug parameter
        slug = self.kwargs.get('category_slug', None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No matching query result was found.")

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class ProductCategoryAPIView(APIView):

    def get(self, request):
        categories = Category.objects.annotate(one=Count('products')).filter(
            one__gt=0)
        serializer = AllCategoriesSerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def search_api(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serialized_products = []
        for product in products:
            product_data = ProductSerializer(product).data
            product_data['image'] = request.build_absolute_uri(
                product.image.url)
            serialized_products.append(product_data)
        return Response(serialized_products)
    else:
        return Response({"products": []})
