from rest_framework import viewsets, permissions
from .models import Cart
from .serializers import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
