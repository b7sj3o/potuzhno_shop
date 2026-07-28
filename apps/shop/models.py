from django.db import models
from django.utils import timezone

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = ProductManager()

    objects = ProductManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
