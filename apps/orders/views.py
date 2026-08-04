from django.shortcuts import render, redirect
from django.contrib import messages
from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem

def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    
    if not cart.items.exists():
        messages.warning(request, "Ваш кошик порожній! Додайте товари перед оформленням.")
        return redirect('shop:product_list')
        
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        # Створюємо замовлення
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            address=address,
            phone=phone,
            total_price=cart.get_total_price()
        )
        
        # Переносимо товари з кошика в замовлення
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            
        # Очищуємо кошик
        cart.items.all().delete()
        
        messages.success(request, f"Замовлення №{order.id} успішно оформлено!")
        return redirect('shop:product_list')
        
    return render(request, 'orders/order_create.html', {'cart': cart})
