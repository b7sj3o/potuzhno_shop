from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # JWT Tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    path('api/shop/', include('apps.shop.api_urls', namespace='api')),
    path('api/shop/', include('apps.reviews.urls', namespace='reviews_api')), # API має свій унікальний namespace 'api'
    path('', include('apps.shop.urls', namespace='shop')),             # Веб має свій namespace 'shop'
    path('accounts/', include('apps.accounts.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
]
