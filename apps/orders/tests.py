import pytest
from apps.orders.models import Order

@pytest.mark.django_db
def test_create_order():
    order = Order.objects.create(
        user=None,
        full_name="Максим Потужний",
        address="м. Київ, вул. Хрещатик, 1",
        phone="+380991112233",
        total_price=1500.00
    )
    assert order.id is not None
    assert order.total_price == 1500.00
