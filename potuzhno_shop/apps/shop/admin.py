from django.contrib import admin

from .models import Category, Product, Size, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}     # slug сам заповнюється з name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category__name", "price", "is_active")
    prepopulated_fields = {"slug": ("name",)}     # slug сам заповнюється з name
    list_filter = ("category", "is_active")
    search_fields = ("name", )


admin.site.register(Size)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", )
