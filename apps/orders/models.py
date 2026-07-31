from django.db import models
from django.contrib.auth.models import User
from apps.shop.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('confirmed', 'Підтверджено'),
        ('sent', 'Відправлено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    city = models.CharField(max_length=100, verbose_name='Місто', blank=True, null=True)
    post_office = models.CharField(max_length=255, verbose_name='Відділення пошти', blank=True, null=True)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)
    customer_name = models.CharField(max_length=255, verbose_name='Ім’я клієнта', blank=True, null=True)

    def __str__(self):
        return f'Замовлення #{self.id} - {self.customer_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
