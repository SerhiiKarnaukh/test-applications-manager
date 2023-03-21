from django.urls import path, include

from product import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/',
         views.ProductAPIDetail.as_view()),
    path('submit_review/<int:product_id>/',
         views.submit_review,
         name='submit_review'),
]
