content = open('potuzhno_shop/settings.py', 'r', encoding='utf-8').read()
new_apps = \"INSTALLED_APPS = ['drf_spectacular', 'drf_spectacular_sidecar',\"
if 'drf_spectacular' not in content:
    content = content.replace('INSTALLED_APPS = [', new_apps)
    
settings_add = \"\"\"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Potuzhno Shop API',
    'DESCRIPTION': 'Ваш потужний магазин',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
\"\"\"
with open('potuzhno_shop/settings.py', 'w', encoding='utf-8') as f:
    f.write(content + settings_add)
