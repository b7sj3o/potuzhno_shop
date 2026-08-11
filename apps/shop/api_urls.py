from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.shop.views import ProductViewSet
from apps.shop.models import Size
from rest_framework import viewsets
from apps.shop.serializers.product import ProductSerializer
from apps.shop.models import Product

class SizeSerializer(viewsets.serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class ProductAPISet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

router = DefaultRouter()
router.register(r'products', ProductAPISet, basename='product-list')
router.register(r'sizes', SizeViewSet, basename='size')

urlpatterns = [
    path('', include(router.urls)),
]
