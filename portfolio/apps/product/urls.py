from django.urls import path

from product import views
from .views import FrontPage, contact, about, ProductDetail, CategoryDetail, ProductSearchListView

# app_name = 'taberna'

urlpatterns = [
    path('', FrontPage.as_view(), name='frontpage'),
    path('shop/', CategoryDetail.as_view(), name='store'),
    path('category/<slug:slug>/',
         CategoryDetail.as_view(),
         name='category_detail'),
    path('category/<slug:category_slug>/<slug:slug>/',
         ProductDetail.as_view(),
         name='product_detail'),
    path('submit_review/<int:product_id>/',
         views.submit_review,
         name='submit_review'),
    path('search/', ProductSearchListView.as_view(), name='search'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    # for Django Rest Framework
    path('api/v1/latest-products/', views.LatestProductsAPIList.as_view()),
    path('api/v1/products/search/', views.search_api),
    path('api/v1/products/<slug:category_slug>/<slug:product_slug>/',
         views.ProductAPIDetail.as_view()),
    path('api/v1/products/<slug:category_slug>/',
         views.CategoryAPIDetail.as_view()),
    path('api/v1/product-categories/', views.ProductCategoryAPIView.as_view()),
]
