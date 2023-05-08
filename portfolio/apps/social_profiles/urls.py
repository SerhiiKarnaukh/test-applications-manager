from django.urls import path

from . import api

app_name = 'social_profiles'

urlpatterns = [
    path('friends/<slug:slug>/', api.friends, name='friends'),
    path('friends/<slug:slug>/request/',
         api.send_friendship_request,
         name='send_friendship_request'),
    path('friends/<slug:slug>/<str:status>/',
         api.handle_request,
         name='handle_request'),
]
