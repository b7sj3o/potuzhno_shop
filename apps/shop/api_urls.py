from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import serializers
from apps.shop.views import ProductViewSet
from apps.shop.models import Size

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class SizeViewSet(DefaultRouter.ViewSet if hasattr(DefaultRouter, 'ViewSet') else __import__('rest_framework').viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

from rest_framework import viewsets
from apps.shop.serializers.product import ProductSerializer
from apps.shop.models import Product

# Оновлений ProductViewSet з lookup_field = "slug"
class FixedProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

router = DefaultRouter()
router.register(r'products', FixedProductViewSet, basename='product-api')
router.register(r'sizes', SizeViewSet, basename='size-api')

urlpatterns = [
    path('', include(router.urls)),
]
