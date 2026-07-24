path = 'potuzhno_shop/settings.py'
content = open(path, 'r', encoding='utf-8').read()
new_db = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''
import re
new_content = re.sub(r'DATABASES = \{.*?\}', new_db, content, flags=re.DOTALL)
open(path, 'w', encoding='utf-8').write(new_content)
print('DATABASE SWITCHED TO SQLITE SUCCESSFULLY!')
