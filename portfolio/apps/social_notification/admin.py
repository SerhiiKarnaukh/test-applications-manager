from django.contrib import admin
from .models import Notification


class NotificationAdminModel(admin.ModelAdmin):
    list_display = ('created_at',)
    ordering = ('created_at',)


admin.site.register(Notification, NotificationAdminModel)
