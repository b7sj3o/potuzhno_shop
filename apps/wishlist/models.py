from django.db import models
from django.contrib.auth.models import User
from apps.shop.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'wishlist'
        unique_together = ('user', 'product')
        verbose_name = 'Обраний товар'
        verbose_name_plural = 'Обрані товари'

    def __str__(self):
        return f"{self.user.username} -> {self.product.name}"
