import os
import re

with open('template_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix active sidebar
content = content.replace('<li class="sub-nav-item active" onclick="location.href=\'notice.html\'">공지 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'notice.html\'">공지 관리</li>')
content = content.replace('<li class="sub-nav-item" onclick="location.href=\'mail_all.html\'">우편 관리</li>', '<li class="sub-nav-item active" onclick="location.href=\'mail_all.html\'">우편 관리</li>')

# Update page LNB using regex
new_lnb = """<div class="page-lnb">
            <a href="mail_all.html" class="page-lnb-item">전체 우편 발송</a>
            <a href="mail_individual.html" class="page-lnb-item">개별 우편 발송</a>
            <a href="mail_template.html" class="page-lnb-item active">템플릿 관리</a>
        </div>"""
content = re.sub(r'<div class="page-lnb">.*?</div>', new_lnb.strip(), content, flags=re.DOTALL)

# Update links back to mail_template.html instead of template.html
content = content.replace("location.href='template.html'", "location.href='mail_template.html'")

# Update title texts
content = content.replace('<title>Gravity Admin Tools - 공지 관리</title>', '<title>Gravity Admin Tools - 우편 관리</title>')
content = content.replace('<div class="form-section-title">템플릿 등록/수정</div>', '<div class="form-section-title">우편 템플릿 등록/수정</div>')

with open('mail_template_form.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created mail_template_form.html")
