import pytest
from django.contrib.auth import get_user_model
from apps.reviews.models import Review
from apps.shop.models import Product, Category

User = get_user_model()

@pytest.mark.django_db
def test_product_review_rating():
    cat = Category.objects.create(name="Футболки", slug="t-shirts")
    product = Product.objects.create(name="Базова Футболка", price=500.00, category=cat)
    user = User.objects.create_user(username="reviewer", password="password123")
    review = Review.objects.create(user=user, product=product, rating=5, text="Чудова якість!")
    assert review.rating == 5
    assert review.text == "Чудова якість!"
