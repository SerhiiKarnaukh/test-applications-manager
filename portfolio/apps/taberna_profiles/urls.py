from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activate-result/', views.activate_result, name='activate_result'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('forgot_password/', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/',
         views.resetpassword_validate,
         name='resetpassword_validate'),
    path('reset_password/', views.resetPassword, name='resetPassword'),
    path('change_password/', views.change_password, name='change_password'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/',
         views.order_detail,
         name='order_detail'),

    # API
    path('api/register/', api.TabernaProfileCreateView.as_view(), name='taberna-api-register'),
    path('api/v1/orders/', api.UserOrdersListView.as_view(), name="taberna-api-user-orders"),
    path('api/v1/token/', api.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
