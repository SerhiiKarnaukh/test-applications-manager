from django.urls import path

from . import api

urlpatterns = [
    # http://127.0.0.1:8000/api/social-posts/
    path('', api.post_list, name='post_list'),
    path('profile/<slug:slug>/',
         api.post_list_profile,
         name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
]
