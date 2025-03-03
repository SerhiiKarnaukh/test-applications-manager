from rest_framework import generics, status
from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from .serializers import ProductSerializer, CategorySerializer, AllCategoriesSerializer, ReviewRatingSerializer
from .models import Product, Category, ReviewRating, Variation


class LatestProductsAPIList(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True).exclude(
        stripe_product_id__isnull=True).exclude(stripe_product_id="")[:6]
    serializer_class = ProductSerializer


class ProductAPIDetail(generics.RetrieveAPIView):
    lookup_url_kwarg = 'product_slug'
    lookup_field = 'slug'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id).exclude(
            stripe_product_id__isnull=True).exclude(stripe_product_id="")
        reviews = ReviewRating.objects.filter(product=product, status=True)

        variations = {
            "colors": Variation.objects.colors().filter(product=product).values('id', 'variation_value'),
            "sizes": Variation.objects.sizes().filter(product=product).values('id', 'variation_value'),
        }

        data = {
            "product": self.get_serializer(product).data,
            "related_products": ProductSerializer(
                related_products, many=True, context={"request": request}
            ).data,
            "reviews": ReviewRatingSerializer(reviews, many=True).data,
            "variations": variations,
        }
        return Response(data)


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
            Q(name__icontains=query) | Q(description__icontains=query)
        ).filter(
            is_available=True
        ).exclude(
            stripe_product_id__isnull=True
        ).exclude(
            stripe_product_id=""
        )
        serialized_products = []
        for product in products:
            product_data = ProductSerializer(product).data
            product_data['image'] = request.build_absolute_uri(
                product.image.url)
            serialized_products.append(product_data)
        return Response(serialized_products)
    else:
        return Response({"products": []})
