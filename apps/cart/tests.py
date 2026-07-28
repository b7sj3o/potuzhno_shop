import pytest
from django.contrib.auth import get_user_model
from apps.cart.models import Cart, CartItem
from apps.shop.models import Product, Category

User = get_user_model()

@pytest.mark.django_db
def test_cart_item_addition():
    cat = Category.objects.create(name="Худі", slug="hoodies")
    product = Product.objects.create(name="Оверсайз Худі", price=1200.00, category=cat)
    user = User.objects.create_user(username="cartuser", password="password123")
    cart = Cart.objects.create(user=user)
    item = CartItem.objects.create(cart=cart, product=product, quantity=2)
    assert item.product.name == "Оверсайз Худі"
    assert item.quantity == 2
