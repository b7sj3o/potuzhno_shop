import os
import django

# 1. Ініціалізуємо налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'potuzhno_shop.settings')
django.setup()

# 2. Тепер безпечно імпортувати моделі
from apps.shop.models import Product

p = Product.objects.first()
if p:
    print(f'Товар {p.name} знайдено, статус: активний')
    p.soft_delete()
    print('Товар видалено (Soft Delete)')
    
    p_check = Product.objects.filter(id=p.id).first()
    if not p_check:
        print('Успіх: Product.objects більше не бачить видалений товар')
    
    p.restore()
    p_check = Product.objects.filter(id=p.id).first()
    if p_check:
        print('Успіх: Товар успішно відновлено')
else:
    print('Товарів у базі не знайдено (створіть хоча б один через адмінку)')