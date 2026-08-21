from django.db import models
from django.contrib.auth import get_user_model
from apps.shop.models import Product

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Користувач')
    full_name = models.CharField(max_length=255, verbose_name='ПІБ')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Загальна ціна')
    status = models.CharField(max_length=20, default='pending', verbose_name='Статус')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Замовлення')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
