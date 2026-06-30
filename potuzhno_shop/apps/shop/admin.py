from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}     # slug сам заповнюється з name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active")
    prepopulated_fields = {"slug": ("name",)}     # slug сам заповнюється з name
    list_filter = ("category", "is_active")
    search_fields = ("name", )