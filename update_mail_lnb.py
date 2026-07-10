import os
import shutil

# 1. Create mail_template.html from template.html
with open('template.html', 'r', encoding='utf-8') as f:
    tpl_html = f.read()

# Fix active sidebar
tpl_html = tpl_html.replace('<li class="sub-nav-item active" onclick="location.href=\'notice.html\'">공지 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'notice.html\'">공지 관리</li>')
tpl_html = tpl_html.replace('<li class="sub-nav-item" onclick="location.href=\'mail_all.html\'">우편 관리</li>', '<li class="sub-nav-item active" onclick="location.href=\'mail_all.html\'">우편 관리</li>')

# Fix breadcrumb
tpl_html = tpl_html.replace('WEB <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 공지 관리', 'WEB <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 우편 관리')

# Remove the old notice LNB and inject the mail LNB
new_lnb = """
        <div class="page-lnb">
            <a href="mail_all.html" class="page-lnb-item">전체 우편 발송</a>
            <a href="mail_individual.html" class="page-lnb-item">개별 우편 발송</a>
            <a href="mail_template.html" class="page-lnb-item active">템플릿 관리</a>
        </div>
"""

# Replace page-lnb in tpl_html
import re
tpl_html = re.sub(r'<div class="page-lnb">.*?</div>', new_lnb.strip(), tpl_html, flags=re.DOTALL)

# Replace '새 템플릿' target to mail_template_form.html (even if we don't create it yet, it's correct)
tpl_html = tpl_html.replace("location.href='template_form.html'", "location.href='mail_template_form.html'")

with open('mail_template.html', 'w', encoding='utf-8') as f:
    f.write(tpl_html)


# 2. Update LNB in mail_all.html, mail_individual.html, mail_all_form.html
mail_files = ['mail_all.html', 'mail_individual.html', 'mail_all_form.html']
for m_file in mail_files:
    with open(m_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check current active item
    is_all = 'mail_all.html" class="page-lnb-item active"' in content or m_file == 'mail_all_form.html'
    is_ind = 'mail_individual.html" class="page-lnb-item active"' in content
    
    act_all = ' active' if is_all else ''
    act_ind = ' active' if is_ind else ''
    
    updated_lnb = f"""<div class="page-lnb">
                <a href="mail_all.html" class="page-lnb-item{act_all}">전체 우편 발송</a>
                <a href="mail_individual.html" class="page-lnb-item{act_ind}">개별 우편 발송</a>
                <a href="mail_template.html" class="page-lnb-item">템플릿 관리</a>
            </div>"""
            
    content = re.sub(r'<div class="page-lnb">.*?</div>', updated_lnb, content, flags=re.DOTALL)
    
    # 3. Add text below select in mail_all_form.html
    if m_file == 'mail_all_form.html':
        old_select = """<select class="form-control" style="width: 300px;">
                        <option>템플릿 선택</option>
                        <option>[1] Mailbox_01</option>
                        <option>[100] Mailbox_02</option>
                    </select>"""
        new_select = """<select class="form-control" style="width: 300px;">
                        <option>1000</option>
                        <option>[1] Mailbox_01</option>
                        <option>[100] Mailbox_02</option>
                    </select>
                    <div style="font-size: 13px; color: #64748B; margin-top: 8px;">제목키 Mail_Reward_Basic_Title · 본문키 Mail_Reward_Basic_Desc · 유저 언어로 자동 현지화</div>"""
        
        content = content.replace(old_select, new_select)
        
    with open(m_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Created mail_template.html and updated LNBs/Form info.")
