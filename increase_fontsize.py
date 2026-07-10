import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

def add_two(match):
    size = int(match.group(1))
    return f"font-size: {size + 2}px"

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = re.sub(r'font-size:\s*(\d+)px', add_two, content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)

print("Font sizes increased by 2px in all HTML files.")
