from .models import Order, OrderItem

def create_order(items_data):
    # Логіка створення замовлення
    order = Order.objects.create()
    for item in items_data:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity']
        )
    return order
