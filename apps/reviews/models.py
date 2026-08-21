from django.db import models
from django.contrib.auth import get_user_model
from apps.shop.models import Product

User = get_user_model()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Користувач')
    rating = models.PositiveSmallIntegerField(verbose_name='Оцінка (1-5)')
    comment = models.TextField(verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        unique_together = ('product', 'user')

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', verbose_name='Користувач')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by', verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')

    class Meta:
        verbose_name = 'Обране'
        verbose_name_plural = 'Обране'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"
