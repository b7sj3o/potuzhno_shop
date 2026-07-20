from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .services import create_order_from_cart
from apps.cart.models import Cart

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        address = self.request.data.get('address')
        create_order_from_cart(self.request.user, cart, address)
