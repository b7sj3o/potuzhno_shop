app_name = 'api'
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from apps.shop.models import Product, Size
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ProductAPISet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

router = DefaultRouter()
router.register(r'products', ProductAPISet, basename='product')
router.register(r'sizes', SizeViewSet, basename='size')

urlpatterns = [
    path('', include(router.urls)),
]
