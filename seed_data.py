import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'potuzhno_shop.settings')
django.setup()

from apps.shop.models import Category, Product, ProductVariant

category, _ = Category.objects.get_or_create(name='Одяг')
product, created = Product.objects.get_or_create(
    name='Потужна футболка', 
    category=category, 
    defaults={'description': 'Крута футболка', 'price': 500}
)
if not created and product.price is None:
    product.price = 500
    product.save()

for size in ['S', 'M', 'L', 'XL']:
    ProductVariant.objects.get_or_create(product=product, size=size, defaults={'stock': 10})

print('Наповнення завершено!')
