from django.contrib import admin
from .models import Product, Category, Brand, Size

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'brand', 'audience')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
