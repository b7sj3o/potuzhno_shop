from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from graphene_django.views import GraphQLView
from apps.shop.schema import schema

urlpatterns = [
    path('api/accounts/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/', admin.site.urls),
    path('api/shop/', include('apps.shop.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
urlpatterns += [path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')]
