import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

def update_sidebar(html, filename):
    index_active = ' active' if filename == 'index.html' else ''
    notice_active = ' active' if filename in ['notice.html', 'notice_form.html', 'template.html', 'template_form.html'] else ''
    maint_active = ' active' if filename == 'maintenance.html' else ''
    mail_active = ' active' if filename in ['mail_all.html', 'mail_individual.html'] else ''

    new_sidebar = f"""<ul class="sub-nav-list">
                        <li class="sub-nav-item{index_active}" onclick="location.href='index.html'">사전예약 관리</li>
                        <li class="sub-nav-item{notice_active}" onclick="location.href='notice.html'">공지 관리</li>
                        <li class="sub-nav-item{maint_active}" onclick="location.href='maintenance.html'">점검 관리</li>
                        <li class="sub-nav-item{mail_active}" onclick="location.href='mail_all.html'">우편 관리</li>
                    </ul>"""
    
    html = re.sub(r'<ul class="sub-nav-list">.*?</ul>', new_sidebar, html, flags=re.DOTALL)
    return html

css = """
        .page-lnb {
            display: flex;
            gap: 24px;
            border-bottom: 1px solid #CBD5E1;
            margin-bottom: 24px;
            padding-bottom: 0;
            margin-top: -10px;
        }
        .page-lnb-item {
            font-size: 14px;
            font-weight: 700;
            color: #94A3B8;
            padding-bottom: 12px;
            cursor: pointer;
            text-decoration: none;
            position: relative;
        }
        .page-lnb-item.active {
            color: var(--admin-tools-blue);
        }
        .page-lnb-item.active::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--admin-tools-blue);
        }
        .page-lnb-item:hover:not(.active) {
            color: #475569;
        }
"""

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Update the left sidebar
    content = update_sidebar(content, f)
    
    # 2. Text Replacements
    content = content.replace("공지 발송", "공지 관리")
    content = content.replace("점검 알림", "점검 관리")
    # For mail files, make sure the breadcrumb doesn't say "전체 우편 발송" as the parent
    content = content.replace("> 전체 우편 발송", "> 우편 관리")
    content = content.replace("> 개별 우편 발송", "> 우편 관리")

    # 3. Add LNB to Mail Pages
    if f in ['mail_all.html', 'mail_individual.html']:
        mail_all_active = ' active' if f == 'mail_all.html' else ''
        mail_ind_active = ' active' if f == 'mail_individual.html' else ''
        
        lnb_html = f"""
            <div class="page-lnb">
                <a href="mail_all.html" class="page-lnb-item{mail_all_active}">전체 우편 발송</a>
                <a href="mail_individual.html" class="page-lnb-item{mail_ind_active}">개별 우편 발송</a>
            </div>"""
            
        if '.page-lnb {' not in content:
            content = content.replace('</style>', css + '    </style>')
            
        if '<div class="page-lnb">' not in content:
            # We will use regex to find the breadcrumb and insert right after its closing </div>
            content = re.sub(r'(<div class="breadcrumb">.*?</div>)', r'\1\n' + lnb_html, content, flags=re.DOTALL)
            
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Menu renames and LNB additions completed.")
