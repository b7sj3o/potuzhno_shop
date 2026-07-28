from rest_framework import viewsets, permissions
from apps.cart.models import Cart
from apps.cart.serializers.cart_serializers import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

