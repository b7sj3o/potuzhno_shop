import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'potuzhno_shop.settings')
django.setup()

from apps.shop.models import Product, Category

Product.objects.all().delete()
Category.objects.all().delete()

def create_cat(name, slug):
    return Category.objects.create(name=name, slug=slug)

c1 = create_cat('Одяг', 'odyag')
c2 = create_cat('Взуття', 'vzuttya')
c3 = create_cat('Аксесуари', 'aksesuary')
c4 = create_cat('Фітнес та Спорт', 'fitnes-sport')

items = [
    ('Преміум світшот ПОТУЖНО Pro', c1, 1299.00, 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&auto=format&fit=crop&q=80', 'S, M, L, XL', 'Чорний, Сірий, Хакі'),
    ('Спортивні тренувальні штани Flex', c1, 999.00, 'https://images.unsplash.com/photo-1517445312882-bc9910d016b7?w=600&auto=format&fit=crop&q=80', 'M, L, XL', 'Чорний, Синій'),
    ('Кросівки бігові Air Tech X', c2, 2899.00, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80', '41, 42, 43, 44, 45', 'Червоний, Білий, Чорний'),
    ('Футболка компресійна', c1, 699.00, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80', 'S, M, L, XL', 'Чорний, Білий'),
    ('Зимова куртка Storm Shield', c1, 3899.00, 'https://images.unsplash.com/photo-1544441893-675973e31985?w=600&auto=format&fit=crop&q=80', 'M, L, XL, XXL', 'Чорний, Зелений'),
    ('Спортивні шорти Active Run', c1, 599.00, 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=600&auto=format&fit=crop&q=80', 'S, M, L', 'Чорний, Сірий, Червоний'),
    ('Худі класичне оверсайз', c1, 1499.00, 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600&auto=format&fit=crop&q=80', 'M, L, XL', 'Чорний, Бежевий'),
    ('Лосини жіночі Sculpt Pro', c1, 899.00, 'https://images.unsplash.com/photo-1506152983158-b4a74a01c721?w=600&auto=format&fit=crop&q=80', 'XS, S, M, L', 'Чорний, Фіолетовий, Графіт'),
    ('Ветровка ультралегка', c1, 1799.00, 'https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?w=600&auto=format&fit=crop&q=80', 'S, M, L, XL', 'Помаранчевий, Чорний'),
    ('Шкарпетки спортивні високі (3 шт)', c3, 349.00, 'https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=600&auto=format&fit=crop&q=80', 'Універсальний (39-45)', 'Білий, Чорний'),
    ('Кепка бейсболка Runner', c3, 499.00, 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=600&auto=format&fit=crop&q=80', 'Reg', 'Чорний, Білий, Оранжевий'),
    ('Рюкзак спортивний 25л', c3, 1899.00, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80', 'One Size', 'Чорний, Сірий'),
    ('Спортивний топ жіночий', c1, 699.00, 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=600&auto=format&fit=crop&q=80', 'S, M, L', 'Чорний, Рожевий, Білий'),
    ('Костюм спортивний велюровий', c1, 2599.00, 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&auto=format&fit=crop&q=80', 'S, M, L, XL', 'Бежевий, Чорний, Сірий'),
    ('Футболка оверсайз Urban', c1, 799.00, 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600&auto=format&fit=crop&q=80', 'S, M, L, XL', 'Білий, Чорний, Оливковий'),
    ('Поло тенісне Active', c1, 999.00, 'https://images.unsplash.com/photo-1625910513418-7c47146e2f1e?w=600&auto=format&fit=crop&q=80', 'M, L, XL', 'Білий, Синій, Чорний'),
    ('Жилет утеплений Gilet', c1, 1699.00, 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=600&auto=format&fit=crop&q=80', 'M, L, XL', 'Чорний, Синій'),
    ('Штани карго Techwear', c1, 1999.00, 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&auto=format&fit=crop&q=80', 'S, M, L, XL', 'Чорний, Хакі'),
    ('Кросівки Trail Master', c2, 3199.00, 'https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=600&auto=format&fit=crop&q=80', '41, 42, 43, 44', 'Коричневий, Чорний'),
    ('Сумка на пояс бананка', c3, 449.00, 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80', 'One Size', 'Чорний, Червоний'),
    ('Рушник з мікрофібри спортивний', c4, 399.00, 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80', 'L (80x130 см)', 'Синій, Сірий, Помаранчевий'),
    ('Пляшка для води Tritan 1L', c4, 499.00, 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80', '1000 мл', 'Прозорий, Чорний'),
    ('Килимок для йоги та фітнесу', c4, 899.00, 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=600&auto=format&fit=crop&q=80', 'Стандарт (10 мм)', 'Фіолетовий, Чорний, Зелений'),
    ('Фітнес-резинки (набір 5 шт)', c4, 399.00, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop&q=80', 'Full Set', 'Різнокольорові'),
    ('Спортивні нарукавники', c4, 299.00, 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&auto=format&fit=crop&q=80', 'S/M, L/XL', 'Чорний, Білий'),
    ('Баф-снуд мультифункціональний', c3, 249.00, 'https://images.unsplash.com/photo-1607345366928-199ef26cfe3e?w=600&auto=format&fit=crop&q=80', 'One Size', 'Чорний, Камуфляж'),
    ('Рукавички для фітнесу Pro', c4, 549.00, 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&auto=format&fit=crop&q=80', 'M, L, XL', 'Чорний, Червоний'),
    ('Шейкер для протеїну 700мл', c4, 329.00, 'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=600&auto=format&fit=crop&q=80', '700 мл', 'Чорний, Білий, Помаранчевий'),
    ('Шльопанці Pool Slide', c2, 699.00, 'https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=600&auto=format&fit=crop&q=80', '40, 41, 42, 43, 44', 'Чорний, Білий'),
    ('Спортивна куртка-дощовик', c1, 2199.00, 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600&auto=format&fit=crop&q=80', 'M, L, XL', 'Жовтий, Чорний')
]

for name, cat, price, img, sizes, colors in items:
    desc = f'Розміри: {sizes} | Кольори: {colors}. Преміальна якість для максимальних досягнень.'
    Product.objects.create(name=name, category=cat, description=desc, price=price, image=img)

print('30 преміальних товарів успішно створено!')
