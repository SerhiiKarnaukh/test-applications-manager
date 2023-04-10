from django.urls import path

from core.views import contact, about
from product.views import ProductDetail, CategoryDetail, ProductSearchListView

urlpatterns = [
    path('', CategoryDetail.as_view(), name='store'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('category/<slug:slug>/',
         CategoryDetail.as_view(),
         name='category_detail'),
    path('category/<slug:category_slug>/<slug:slug>/',
         ProductDetail.as_view(),
         name='product_detail'),
    path('search/', ProductSearchListView.as_view(), name='search'),
]
