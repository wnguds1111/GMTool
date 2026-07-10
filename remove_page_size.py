import os

files = ['notice.html', 'template.html', 'mail_all.html', 'mail_individual.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact strings to revert
    new_str = '<span style="color: #94A3B8; margin-right: 16px;">(전체 : 10)</span>\n                <select class="form-control" style="width: auto;"><option>20개씩 보기</option><option>50개씩 보기</option></select>'
    new_str_tpl = '<span style="color: #94A3B8; margin-right: 16px;">(전체 : 3)</span>\n                <select class="form-control" style="width: auto;"><option>20개씩 보기</option><option>50개씩 보기</option></select>'
    
    old_str = '<span style="color: #94A3B8; margin-right: 10px;">(전체 : 10)</span>'
    old_str_tpl = '<span style="color: #94A3B8; margin-right: 10px;">(전체 : 3)</span>'
    
    content = content.replace(new_str, old_str)
    content = content.replace(new_str_tpl, old_str_tpl)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Removed 20 items per page dropdown.")
