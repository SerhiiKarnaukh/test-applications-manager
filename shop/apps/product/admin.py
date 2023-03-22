from django.contrib import admin
import admin_thumbnails

from .models import Category, Product, Variation, ReviewRating, ProductGallery


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ordering')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    list_editable = ('ordering', )
    prepopulated_fields = {"slug": ("name", )}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_available', 'stock',
                    'date_added', 'image')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'stock')
    list_filter = ('is_available', 'date_added', 'category')
    prepopulated_fields = {"slug": ("name", )}
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value',
                    'is_active')
    list_editable = ('is_active', )
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
