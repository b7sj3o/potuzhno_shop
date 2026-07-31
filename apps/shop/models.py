from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveIntegerField(default=1, choices=RATING_CHOICES)
    text = models.TextField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.product} - {self.rating}"


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True, deleted_at__isnull=True)

    def with_rating(self):
        return self.annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews", distinct=True),
        )


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Product(models.Model):
    AUDIENCE_CHOICES = [
        ("unisex", "Унісекс"),
        ("man", "Чоловіче"),
        ("woman", "Жіноче"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=False,
        related_name="products",
        related_query_name="product"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, verbose_name="Пропонований?")

    sku = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        null=True, blank=True,
        verbose_name="Артикул",
        help_text="Унікальний код товару, напр. HD-OVR-001",
    )

    audience = models.CharField(
        max_length=10,
        choices=AUDIENCE_CHOICES,
        default="unisex",
        verbose_name="Аудиторія"
    )

    stock = models.PositiveIntegerField(default=0, verbose_name="Залишок")
    sizes = models.ManyToManyField(Size, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products", null=True, blank=True)

    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    objects = ProductManager()
