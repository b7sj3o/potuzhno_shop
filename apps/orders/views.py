from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework import viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer
from apps.shop.models import Product
from apps.cart.models import Cart

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

def checkout_view(request):
    cart = request.session.get('cart', {})
    
    # Підтягуємо кошик з БД, якщо сесія порожня, а користувач авторизований
    if not cart and request.user.is_authenticated:
        db_cart = Cart.objects.filter(user=request.user).first()
        if db_cart:
            cart = {
                str(item.product.id): {
                    'name': item.product.name,
                    'price': float(item.product.price),
                    'quantity': item.quantity,
                    'image': item.product.image.url if hasattr(item.product, 'image') and item.product.image else ''
                } for item in db_cart.items.all()
            }

    if request.method == 'POST':
        if not cart:
            messages.warning(request, "Ваш кошик порожній!")
            return redirect('cart:cart_detail')
            
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        branch = request.POST.get('branch', '')
        address = f"{city}, {branch}"
        payment_method = request.POST.get('payment_method', 'cash')
        promo_code = request.POST.get('promo_code', '')
        
        user = request.user if request.user.is_authenticated else None
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        
        order = Order.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            branch=branch,
            payment_method=payment_method,
            promo_code=promo_code,
            total_price=total_price,
            status='Pending'
        )
        
        for pid, item in cart.items():
            product = Product.objects.filter(id=int(pid)).first()
            if product:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']
                )
                
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, f"Замовлення №{order.id} успішно оформлено!")
        return render(request, 'orders/success.html', {'order': order})
        
    if not cart:
        messages.warning(request, "Ваш кошик порожній!")
        return redirect('cart:cart_detail')
        
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'orders/checkout.html', {'cart': cart, 'total_price': total_price})
