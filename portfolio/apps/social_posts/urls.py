from django.urls import path

from . import api

app_name = 'social_posts'

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('profile/<slug:slug>/',
         api.post_list_profile,
         name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('search/', api.search, name='search'),
]
