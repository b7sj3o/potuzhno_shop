path = 'potuzhno_shop/settings.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if 'DATABASES = {' in line:
        skip = True
        new_lines.append('DATABASES = {\n')
        new_lines.append('    \'default\': {\n')
        new_lines.append('        \'ENGINE\': \'django.db.backends.sqlite3\',\n')
        new_lines.append('        \'NAME\': BASE_DIR / \'db.sqlite3\',\n')
        new_lines.append('    }\n')
        new_lines.append('}\n')
    elif skip:
        if '}' in line:
            skip = False
        continue
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('settings.py FIXED SUCCESSFULLY!')
