import os
import re

# 1. Create mail_all_detail.html
with open('mail_all_form.html', 'r', encoding='utf-8') as f:
    form_html = f.read()

detail_html = form_html.replace('전체 우편 작성', '전체 우편 상세')
detail_html = detail_html.replace('<input ', '<input readonly ')
detail_html = detail_html.replace('<textarea ', '<textarea readonly ')
detail_html = detail_html.replace('<select ', '<select disabled ')

old_buttons = """<button class="btn btn-outline" style="padding: 10px 24px;" onclick="location.href='mail_all.html'">취소</button>
            <button class="btn btn-primary" style="padding: 10px 24px;" onclick="location.href='mail_all.html'">등록</button>"""
new_buttons = """<button class="btn btn-primary" style="padding: 10px 24px;" onclick="location.href='mail_all.html'">목록</button>"""
detail_html = detail_html.replace(old_buttons, new_buttons)

with open('mail_all_detail.html', 'w', encoding='utf-8') as f:
    f.write(detail_html)

# 2. Create mail_individual_detail.html
with open('mail_individual_form.html', 'r', encoding='utf-8') as f:
    indiv_form_html = f.read()

indiv_detail_html = indiv_form_html.replace('단건 우편 작성', '단건 우편 상세')
indiv_detail_html = indiv_detail_html.replace('<input ', '<input readonly ')
indiv_detail_html = indiv_detail_html.replace('<textarea ', '<textarea readonly ')
indiv_detail_html = indiv_detail_html.replace('<select ', '<select disabled ')

old_indiv_buttons = """<button class="btn btn-outline" style="padding: 10px 24px;" onclick="location.href='mail_individual.html'">취소</button>
            <button class="btn btn-primary" style="padding: 10px 24px;" onclick="location.href='mail_individual.html'">발송</button>"""
new_indiv_buttons = """<button class="btn btn-primary" style="padding: 10px 24px;" onclick="location.href='mail_individual.html'">목록</button>"""
indiv_detail_html = indiv_detail_html.replace(old_indiv_buttons, new_indiv_buttons)

with open('mail_individual_detail.html', 'w', encoding='utf-8') as f:
    f.write(indiv_detail_html)

# 3. Update mail_individual.html "수정 / 삭제" -> "상세"
with open('mail_individual.html', 'r', encoding='utf-8') as f:
    indiv_html = f.read()

indiv_html = re.sub(
    r'<button class="btn btn-outline" style="padding: 4px 12px;">수정</button>\s*<button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>',
    """<button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='mail_individual_detail.html'">상세</button>""",
    indiv_html
)

with open('mail_individual.html', 'w', encoding='utf-8') as f:
    f.write(indiv_html)

# 4. Update fix_mail_table4.py for cursor not-allowed
with open('fix_mail_table4.py', 'r', encoding='utf-8') as f:
    fix_py = f.read()

if 'cursor: not-allowed' not in fix_py:
    fix_py = fix_py.replace(
        'border: 1px solid #16A34A;" disabled>',
        'border: 1px solid #16A34A; cursor: not-allowed;" disabled>'
    )
    fix_py = fix_py.replace(
        'btn.style.borderColor = "#16A34A";',
        'btn.style.borderColor = "#16A34A";\n                btn.style.cursor = "not-allowed";'
    )
    with open('fix_mail_table4.py', 'w', encoding='utf-8') as f:
        f.write(fix_py)

print("Created details pages, updated mail_individual, and updated fix_mail_table4.py")
