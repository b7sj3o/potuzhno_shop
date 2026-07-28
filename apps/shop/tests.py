from django.test import TestCase
from apps.shop.models import Category, Product

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тест Категорія', slug='test-cat')
        self.product = Product.objects.create(
            name='Тестовий товар',
            category=self.category,
            description='Опис тестового товару',
            price=150.00
        )

    def cigar_test_product_creation(self):
        self.assertEqual(self.product.name, 'Тестовий товар')
        self.assertEqual(self.product.price, 150.00)
        self.assertTrue(self.product.deleted_at is None)

    def test_soft_delete(self):
        self.product.soft_delete()
        self.assertIsNotNone(self.product.deleted_at)
        # Перевіряємо що кастомний objects менеджер не бачить видалений
        self.assertNotIn(self.product, Product.objects.all())
