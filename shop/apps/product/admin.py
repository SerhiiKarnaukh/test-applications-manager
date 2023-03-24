from django.contrib import admin
import admin_thumbnails

from .models import Category, Product, Variation, ReviewRating, ProductGallery


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'ordering',
    )
    list_display_links = ('name', )
    search_fields = ('name', )
    list_editable = ('ordering', )
    prepopulated_fields = {"slug": ("name", )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'is_available',
        'stock',
        'date_added',
        'image',
    )
    list_display_links = ('name', )
    search_fields = (
        'name',
        'description',
    )
    list_editable = (
        'is_available',
        'stock',
        'price',
    )
    list_filter = (
        'is_available',
        'date_added',
        'category',
    )
    prepopulated_fields = {"slug": ("name", )}
    inlines = [ProductGalleryInline]


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'is_active',
    )
    list_editable = ('is_active', )
    list_filter = (
        'product',
        'variation_category',
        'variation_value',
    )


admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
