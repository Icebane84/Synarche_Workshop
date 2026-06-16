path = 'axion-core/standards/mypy.ini'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

content = content.replace('open-notebook/|archives/', 'open-notebook/|tests/|archives/')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("mypy.ini tests exclusion added.")
