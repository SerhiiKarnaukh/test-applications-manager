from rest_framework import serializers

from .models import Category, Product, ProductGallery


class ProductGallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductGallery
        fields = (
            "id",
            "image",
        )


class ProductSerializer(serializers.ModelSerializer):

    productgallery = ProductGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "image",
            "get_absolute_url",
            "description",
            "price",
            "productgallery",
        )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        product = Product.objects.create(**validated_data)
        for image_data in images_data.values():
            ProductGallery.objects.create(product=product, image=image_data)
        return product


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )


class AllCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
        )
