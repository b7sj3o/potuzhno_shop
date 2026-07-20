from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', lambda request: redirect('swagger-ui')),
    path('admin/', admin.site.urls),
    path('api/shop/', include('apps.shop.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
