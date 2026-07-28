import pytest
from apps.orders.models import Order

@pytest.mark.django_db
def test_create_order():
    order = Order.objects.create(user_id=None, total_price=1500.0, status='pending')
    assert order.id is not None
