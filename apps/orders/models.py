from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    # додав зв'язок з користувачем
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Користувач")
    # додав ПІБ замовника
    full_name = models.CharField(max_length=255, verbose_name="ПІБ")
    # додав адресу доставки
    address = models.CharField(max_length=255, verbose_name="Адреса", blank=True, null=True)
    # додав статус замовлення
    status = models.CharField(max_length=50, default="new", verbose_name="Статус")
    # додав номер телефону
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    # додав загальну вартість
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    # додав статус оплати
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    # додав дату створення
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f"Замовлення #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    # додав зв'язок із замовленням
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Замовлення")
    # додав продукт
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, verbose_name="Продукт")
    # додав кількість
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    # додав ціну за одиницю
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
