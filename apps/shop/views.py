from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from .services.product_service import soft_delete_product, restore_product

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock']

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        soft_delete_product(self.get_object())
        return Response({'status': 'product soft deleted'})

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        product = Product.all_objects.get(pk=pk)
        restore_product(product)
        return Response({'status': 'product restored'})