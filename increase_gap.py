import os

files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'margin-top: -10px;' in content:
        content = content.replace('margin-top: -10px;', 'margin-top: 16px;')
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Increased the gap between breadcrumb and LNB.")
