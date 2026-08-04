from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.cart.models import Cart, CartItem

def cart_detail(request):
    # Отримуємо кошик для користувача або аноніма
    cart, created = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
