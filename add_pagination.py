import os
import re

css_pagination = """
        .pagination { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 30px; margin-bottom: 20px; }
        .page-link { display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; color: var(--text-dark); text-decoration: none; font-size: 16px; font-weight: 500; transition: all 0.2s; }
        .page-link.active { background-color: var(--admin-tools-blue); color: var(--white); font-weight: 700; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3); }
        .page-link:hover:not(.active) { background-color: #E2E8F0; }
        .page-link i { font-size: 14px; }
"""

css_search = """
        .list-header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .list-search { display: flex; align-items: center; gap: 8px; }
        .list-search select { padding: 8px; border: 1px solid var(--border-color); border-radius: 4px; outline: none; font-size: 15px; }
        .list-search input { padding: 8px; border: 1px solid var(--border-color); border-radius: 4px; width: 200px; outline: none; font-size: 15px; }
"""

pagination_html = """
        <div class="pagination">
            <a href="#" class="page-link"><i class="fa-solid fa-angles-left"></i></a>
            <a href="#" class="page-link active">1</a>
            <a href="#" class="page-link">2</a>
            <a href="#" class="page-link"><i class="fa-solid fa-angles-right"></i></a>
        </div>
"""

# 1. notice.html & template.html
for file in ['notice.html', 'template.html']:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if '.pagination {' not in content:
        content = content.replace('</style>', css_pagination + '    </style>')
    if '<div class="pagination">' not in content:
        content = content.replace('</table>', '</table>\n' + pagination_html)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. mail_all.html & mail_individual.html
mail_files = {
    'mail_all.html': ('전체 우편', 'AccountDB 중앙 등록 후 게임 샤드에 적용', '전체 우편 작성', "location.href='mail_all_form.html'"),
    'mail_individual.html': ('개별 우편', 'AccountDB 사용자 계정 단위로 개별 발송', '개별 우편 작성', '')
}

for file, (title, desc, btn_text, btn_action) action_onclick in zip(mail_files.keys(), mail_files.values()):
    # Unpack the tuple properly
    pass

for file, details in mail_files.items():
    title, desc, btn_text, btn_action = details
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject Pagination CSS
    if '.pagination {' not in content:
        content = content.replace('</style>', css_pagination + '    </style>')
    
    # Inject Search CSS
    if '.list-header-bar {' not in content:
        content = content.replace('</style>', css_search + '    </style>')

    # Append Pagination
    if '<div class="pagination">' not in content:
        content = content.replace('</table>', '</table>\n' + pagination_html)

    # Replace list-header-bar
    old_header = r'<div class="list-header-bar".*?</button>\s*</div>'
    
    onclick_attr = f' onclick="{btn_action}"' if btn_action else ''
    
    new_header = f"""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 20px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px;">{title}</div>
            <div style="font-size: 15px; color: #64748B;">{desc}</div>
        </div>
        <div class="list-header-bar">
            <div class="list-search">
                <span style="color: #94A3B8; margin-right: 10px;">(전체 : 10)</span>
                <select>
                    <option>제목</option>
                </select>
                <input type="text" placeholder="검색어를 입력하세요">
                <button class="btn btn-primary">조회</button>
            </div>
            <div style="display: flex; gap: 8px;">
                <button class="btn btn-primary"{onclick_attr}>{btn_text}</button>
            </div>
        </div>
"""
    if 'class="list-search"' not in content:
        content = re.sub(old_header, new_header.strip(), content, flags=re.DOTALL)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Pagination added and mail list UI synchronized.")
