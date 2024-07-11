from .models import Category
from django.db.models import Count


def menu_categories(request):
    categories = Category.objects.annotate(one=Count('products')).filter(
        one__gt=0)

    return {'menu_categories': categories}


def top_categories(request):
    categories = Category.objects.annotate(one=Count('products')).filter(
        one__gt=0)[:6]

    return {'top_categories': categories}
