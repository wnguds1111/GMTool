import os

files = ['notice.html', 'template.html', 'mail_all.html', 'mail_individual.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if we already have a '20개씩 보기' dropdown
    if '20개씩 보기' not in content:
        old_span = '<span style="color: #94A3B8; margin-right: 10px;">(전체 :'
        new_span = '<select class="form-control" style="width: auto; margin-right: 8px; font-size: 14px;"><option>20개씩 보기</option><option>50개씩 보기</option></select>\n                <span style="color: #94A3B8; margin-right: 10px;">(전체 :'
        
        # We need to find the span and insert the select right before it or after it. 
        # Actually, in list-search, putting it after the (전체: 10) is also good.
        old_str = '<span style="color: #94A3B8; margin-right: 10px;">(전체 : 10)</span>'
        old_str_tpl = '<span style="color: #94A3B8; margin-right: 10px;">(전체 : 3)</span>'
        
        new_str = '<span style="color: #94A3B8; margin-right: 16px;">(전체 : 10)</span>\n                <select class="form-control" style="width: auto;"><option>20개씩 보기</option><option>50개씩 보기</option></select>'
        new_str_tpl = '<span style="color: #94A3B8; margin-right: 16px;">(전체 : 3)</span>\n                <select class="form-control" style="width: auto;"><option>20개씩 보기</option><option>50개씩 보기</option></select>'
        
        content = content.replace(old_str, new_str)
        content = content.replace(old_str_tpl, new_str_tpl)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Added 20 items per page dropdown.")
