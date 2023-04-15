from django.urls import path

from .views import CategoryDetail, ProjectSearchListView, ProjectDetail, ProjectsByTag

app_name = 'core'

urlpatterns = [
    path('', CategoryDetail.as_view(), name='index'),
    path('category/<slug:slug>/',
         CategoryDetail.as_view(),
         name='category_detail'),
    path('category/<slug:category_slug>/<slug:slug>/',
         ProjectDetail.as_view(),
         name='project_detail'),
    path('tag/<str:slug>/', ProjectsByTag.as_view(), name='tag'),
    path('search/', ProjectSearchListView.as_view(), name='search'),
]
