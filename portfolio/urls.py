from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),

    # Djoser
    path('api/v1/auth', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # JWT
    path('api/v1/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/v1/token/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),

    # for Django Templates
    path('cart/', include('cart.urls')),
    path('', include('core.urls')),
    path('store/', include('product.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),

    # DRF
    path('api/social-posts/', include('social_posts.urls')),
    path('api/social-profiles/', include('social_profiles.urls')),
    path('api/social-chat/', include('social_chat.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
