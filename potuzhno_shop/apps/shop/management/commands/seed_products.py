"""
Наповнення каталогу демо-даними для Рівня 8 (щоб було що фільтрувати й гортати).

Запуск:
    python manage.py seed_products

Команда ідемпотентна (get_or_create за slug) — можна запускати повторно без дублів.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.shop.models import Category, Product


CATEGORIES = {
    "hoodies": "Худі",
    "tshirts": "Футболки",
    "sneakers": "Кросівки",
    "pants": "Штани",
    "jackets": "Куртки",
}

# (name, slug, category_slug, price, audience, stock, is_featured, sku)
PRODUCTS = [
    ("Худі Oversize", "hoodie-oversize", "hoodies", "1290.00", "unisex", 20, True, "HD-OVR-001"),
    ("Худі Zip Black", "hoodie-zip-black", "hoodies", "1490.00", "man", 12, False, "HD-ZIP-002"),
    ("Худі Crop", "hoodie-crop", "hoodies", "1190.00", "woman", 8, True, "HD-CRP-003"),
    ("Футболка Basic", "tshirt-basic", "tshirts", "590.00", "unisex", 50, False, "TS-BSC-004"),
    ("Футболка Print", "tshirt-print", "tshirts", "690.00", "man", 30, False, "TS-PRN-005"),
    ("Футболка Slim", "tshirt-slim", "tshirts", "650.00", "woman", 25, True, "TS-SLM-006"),
    ("Кросівки Runner", "sneakers-runner", "sneakers", "2490.00", "unisex", 15, True, "SN-RNR-007"),
    ("Кросівки Trail", "sneakers-trail", "sneakers", "2990.00", "man", 10, False, "SN-TRL-008"),
    ("Кросівки Light", "sneakers-light", "sneakers", "2290.00", "woman", 9, False, "SN-LGT-009"),
    ("Джогери Comfort", "pants-joggers", "pants", "1090.00", "unisex", 18, False, "PN-JGR-010"),
    ("Штани Cargo", "pants-cargo", "pants", "1390.00", "man", 14, True, "PN-CRG-011"),
    ("Легінси Sport", "pants-leggings", "pants", "790.00", "woman", 22, False, "PN-LGS-012"),
    ("Куртка Bomber", "jacket-bomber", "jackets", "2790.00", "unisex", 7, True, "JK-BMB-013"),
    ("Куртка Puffer", "jacket-puffer", "jackets", "3990.00", "man", 5, False, "JK-PFR-014"),
    ("Вітровка Light", "jacket-windbreaker", "jackets", "1690.00", "woman", 11, False, "JK-WND-015"),
]


class Command(BaseCommand):
    help = "Наповнює каталог демо-категоріями та товарами (ідемпотентно)."

    def handle(self, *args, **options):
        cat_objs = {}
        for slug, name in CATEGORIES.items():
            obj, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            cat_objs[slug] = obj

        created = 0
        for name, slug, cat_slug, price, audience, stock, featured, sku in PRODUCTS:
            _, was_created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": cat_objs[cat_slug],
                    "price": Decimal(price),
                    "audience": audience,
                    "stock": stock,
                    "is_featured": featured,
                    "sku": sku,
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f"Готово: категорій {len(cat_objs)}, нових товарів {created} "
            f"(усього в каталозі {Product.objects.count()})."
        ))
