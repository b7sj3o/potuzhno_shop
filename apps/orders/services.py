from .models import Order, OrderItem

def create_order_from_cart(user, cart, address):
    order = Order.objects.create(user=user, address=address)
    total = 0
    for item in cart.items.all():
        price = item.variant.product.price
        OrderItem.objects.create(
            order=order,
            variant=item.variant,
            quantity=item.quantity,
            price=price
        )
        total += price * item.quantity
    
    order.total_price = total
    order.save()
    cart.items.all().delete() # Очищаємо кошик після створення замовлення
    return order
