from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shop/', include('apps.shop.api_urls', namespace='api')), # API має свій унікальний namespace 'api'
    path('', include('apps.shop.urls', namespace='shop')),             # Веб має свій namespace 'shop'
    path('accounts/', include('apps.accounts.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
]
