from django.urls import path

from . import api

app_name = 'social_notification'


urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('read/<uuid:pk>/', api.read_notification, name='read_notification'),
]
