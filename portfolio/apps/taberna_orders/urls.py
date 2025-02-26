from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('order_complete/<int:order_number>/', views.order_complete, name='order_complete'),
    path('order_failed/', views.order_failed, name='order_failed'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),

    # API
    path('api/v1/place_order_stripe_charge/',
         api.PlaceOrderStripeChargeAPIView.as_view(), name='taberna_api_place_order_charge'),
    path('api/v1/place_order_stripe_session/',
         api.PlaceOrderStripeSessionAPIView.as_view(), name='taberna_api_place_order_session'),
    path('api/v1/order_payment_success/',
         api.OrderPaymentSuccessAPIView.as_view(), name='taberna_api_payment_success'),
    path('api/v1/order_payment_failed/',
         api.OrderPaymentFailedAPIView.as_view(), name='taberna_api_payment_failed'),
]
