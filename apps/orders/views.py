from rest_framework import viewsets, permissions
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # додав перевірку для генерації документації swagger
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.cart.models import Cart

class CheckoutView(LoginRequiredMixin, TemplateView):
    # додав відображення сторінки оформлення замовлення
    template_name = 'orders/checkout.html'

    def dispatch(self, request, *args, **kwargs):
        # перевірив наявність товарів у кошику для редіректу
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            from django.shortcuts import redirect
            return redirect('cart:cart_detail')
        return super().dispatch(request, *args, **kwargs)
