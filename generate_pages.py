import re

with open('index.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Clear out the content in the main-content area but keep breadcrumb and page-title
# We can just use a regex to replace everything after <div class="page-title">...</div> up to </div>\n\n</body>
# Wait, let's just do string manipulation.
title_end = base_html.find('</div>', base_html.find('class="page-title"')) + 6
body_end = base_html.rfind('</div>\n\n</body>')

if title_end != -1 and body_end != -1:
    empty_content_html = base_html[:title_end] + '\n\n        <div style="padding: 40px; text-align: center; color: #94A3B8; font-size: 14px; border: 2px dashed #E2E8F0; border-radius: 8px; margin-top: 20px;">콘텐츠 영역 (준비 중)</div>\n    ' + base_html[body_end:]
else:
    empty_content_html = base_html

pages = [
    {
        "file": "notice.html",
        "title": "공지 발송",
        "target": "onclick=\"location.href='notice.html'\""
    },
    {
        "file": "maintenance.html",
        "title": "점검 알림",
        "target": "onclick=\"location.href='maintenance.html'\""
    },
    {
        "file": "mail_all.html",
        "title": "전체 우편 발송",
        "target": "onclick=\"location.href='mail_all.html'\""
    },
    {
        "file": "mail_individual.html",
        "title": "개별 우편 발송",
        "target": "onclick=\"location.href='mail_individual.html'\""
    }
]

for page in pages:
    html = empty_content_html
    
    # Update active class
    # Remove active from index.html
    html = html.replace('class="sub-nav-item active" onclick="location.href=\'index.html\'"', 'class="sub-nav-item" onclick="location.href=\'index.html\'"')
    # Add active to the target
    html = html.replace(f'class="sub-nav-item" {page["target"]}', f'class="sub-nav-item active" {page["target"]}')
    
    # Update title
    html = re.sub(r'<div class="page-title">.*?</div>', f'<div class="page-title">{page["title"]}</div>', html)
    html = re.sub(r'<div class="breadcrumb">.*?</div>', f'<div class="breadcrumb">\n            WEB <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> {page["title"]}\n        </div>', html, flags=re.DOTALL)
    
    with open(page["file"], 'w', encoding='utf-8') as f:
        f.write(html)

print("Pages generated successfully.")
