from .models import Category, Project, Tag
from django.db.models import Count


def menu_categories(request):
    categories = Category.objects.annotate(one=Count('projects')).filter(
        one__gt=0).order_by('title')
    for category in categories:
        category.quantity = Project.objects.filter(category=category).count()

    return {'core_menu_categories': categories}


def core_tags(request):
    tags = Tag.objects.filter(projects__isnull=False).distinct()
    return {'core_tags': tags}
