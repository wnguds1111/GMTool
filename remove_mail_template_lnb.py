import os
import re

files = ['mail_all.html', 'mail_all_form.html', 'mail_individual.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the 템플릿 관리 LNB item
    # It might have class="page-lnb-item" or class="page-lnb-item active"
    # we can use regex to remove the whole line
    content = re.sub(r'\s*<a href="mail_template\.html" class="page-lnb-item[^>]*>템플릿 관리</a>', '', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

# Optionally remove the html files
if os.path.exists('mail_template.html'):
    os.remove('mail_template.html')
if os.path.exists('mail_template_form.html'):
    os.remove('mail_template_form.html')

print("Removed mail_template link from LNB and deleted template files.")
