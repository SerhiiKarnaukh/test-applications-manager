from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),

    # for Django Rest Framework
    # path('api/v1/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('', include('core.urls')),
    path('store/', include('product.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
