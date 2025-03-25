from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from django_ckeditor_5.widgets import CKEditor5Widget
# import admin_thumbnails


from .models import Category, Tag, Project, ProjectGallery


# @admin_thumbnails.thumbnail('image')
class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1


class ProjectAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }


class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    form = ProjectAdminForm
    list_display = (
        'id',
        'title',
        'ordering',
        'slug',
        # 'tags',
        'category',
        'created_at',
        'get_photo',
    )
    list_editable = ('ordering',)
    list_display_links = (
        'id',
        'title',
    )
    search_fields = (
        'title',
        'content',
    )
    list_filter = (
        'created_at',
        'category',
        'tags',
    )
    readonly_fields = (
        'created_at',
        'get_photo',
    )
    fields = (
        'title',
        'ordering',
        'slug',
        'category',
        'tags',
        'content',
        'github_url',
        'view_url',
        'photo',
        'get_photo',
        'created_at',
    )
    ordering = ['ordering', '-created_at']
    prepopulated_fields = {"slug": ("title", )}
    inlines = [ProjectGalleryInline]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="300">')
        return '-'

    get_photo.short_description = 'Image'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
