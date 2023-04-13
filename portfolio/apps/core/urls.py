from django.urls import path

from .views import index, app_detail

urlpatterns = [
    path('', index, name='index'),
    path('app/', app_detail, name='app_detail')
]
