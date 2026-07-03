from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    # icon_path

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    AUDIENCE_CHOICES = [
        ("unisex", "Унісекс"),
        ("man", "Чоловіче"),
        ("woman", "Жіноче"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

