from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.shop.views import ProductViewSet
from apps.shop.models import Size, Product
from apps.shop.serializers.product import ProductSerializer
from rest_framework import viewsets

class SizeSerializer(viewsets.serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

# Явно задаємо basename, щоб DRF створював правильні реверси 'product-list' та 'product-detail'
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'sizes', SizeViewSet, basename='size')

urlpatterns = [
    path('', include(router.urls)),
]
