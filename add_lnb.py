import os
import re

files = ['notice.html', 'notice_form.html', 'template.html', 'template_form.html']

lnb_css = """
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

def add_css(html, css):
    if '.page-lnb {' not in html:
        return html.replace('</style>', css + '    </style>', 1)
    return html

def inject_lnb(html, filename):
    if '<div class="page-lnb">' in html:
        return html

    # Define active states
    notice_active = ' active' if 'notice' in filename else ''
    template_active = ' active' if 'template' in filename else ''

    lnb_html = f"""
        <div class="page-lnb">
            <a href="notice.html" class="page-lnb-item{notice_active}">공지 발송</a>
            <a href="template.html" class="page-lnb-item{template_active}">템플릿 관리</a>
        </div>
"""
    
    # Inject after breadcrumb or at the top of main content
    if '<div class="breadcrumb">' in html:
        # find the end of breadcrumb
        parts = html.split('</div>\n\n        <div class="list-header-bar">')
        if len(parts) > 1:
            return parts[0] + '</div>\n' + lnb_html + '\n        <div class="list-header-bar">' + parts[1]
    
    # If it's a form view, there might not be a breadcrumb, but a form-header-bar
    # Actually notice_form.html and template_form.html don't have breadcrumbs currently.
    # Let's inject it right after <div class="main-content"> (or the first <div> inside it)
    # Wait, notice_form.html starts with:
    # <div class="main-content">
    #     <!-- Form View -->
    #     <div>
    #     <div >
    #         <div class="form-header-bar">
    
    # Let's just find form-header-bar and inject before it
    parts = html.split('<div class="form-header-bar">')
    if len(parts) > 1:
        return parts[0] + lnb_html + '        <div class="form-header-bar">' + parts[1]
        
    return html

for f in files:
    if not os.path.exists(f):
        continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = add_css(content, lnb_css)
    content = inject_lnb(content, f)

    # Specific fix for notice_form.html: Add [템플릿 불러오기] button
    if f == 'notice_form.html':
        target_btn = '<button class="btn btn-secondary" onclick="location.href=\'notice.html\'">뒤로가기</button>'
        replacement = """<div style="display: flex; justify-content: space-between; width: 100%;">
                    <button class="btn btn-secondary" onclick="location.href='notice.html'">뒤로가기</button>
                    <button class="btn btn-outline" style="border-color: var(--admin-tools-blue); color: var(--admin-tools-blue);" onclick="alert('템플릿 불러오기 기능 (준비중)')"><i class="fa-solid fa-file-import" style="margin-right:6px;"></i>템플릿 불러오기</button>
                </div>"""
        
        # We need to replace the content inside form-header-bar
        # Currently: 
        # <div class="form-header-bar">
        #     <button class="btn btn-secondary" onclick="location.href='notice.html'">뒤로가기</button>
        # </div>
        
        if target_btn in content and replacement not in content:
            content = content.replace(target_btn, replacement)
            
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("LNB and Load Template button added successfully.")
