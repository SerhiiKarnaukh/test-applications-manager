from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import Category, Tag, Project


class ProjectAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Project
        fields = '__all__'


class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    form = ProjectAdminForm
    list_display = (
        'id',
        'title',
        'slug',
        # 'tags',
        'category',
        'created_at',
        'get_photo',
    )
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
    prepopulated_fields = {"slug": ("title", )}

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
