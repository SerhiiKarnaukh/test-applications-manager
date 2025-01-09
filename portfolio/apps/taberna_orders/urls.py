from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('order_complete/<int:order_number>/', views.order_complete, name='order_complete'),
    path('order_failed/', views.order_failed, name='order_failed'),

    # API
    path('api/v1/place_order/', api.PlaceOrderAPIView.as_view(), name='taberna_api_place_order'),
]
