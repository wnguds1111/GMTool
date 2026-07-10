import os
import re

css_to_add = """
        .breadcrumb {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .breadcrumb i {
            color: #CBD5E1;
            font-size: 14px;
        }

        .page-lnb {
            display: flex;
            gap: 24px;
            border-bottom: 1px solid #CBD5E1;
            margin-bottom: 24px;
            padding-bottom: 0;
            margin-top: 16px;
        }
        .page-lnb-item {
            font-size: 16px;
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

def process_file(filename, active_tab_index):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing .breadcrumb css to avoid duplication if it exists, or just append
    if '.page-lnb {' not in content:
        content = content.replace('</style>', css_to_add + '\n    </style>')

    html_new = f"""<div class="breadcrumb">
            WEB <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 점검 관리
        </div>

        <div class="page-lnb">
            <a href="maintenance.html" class="page-lnb-item {'active' if active_tab_index == 0 else ''}">점검 관리</a>
            <a href="whitelist.html" class="page-lnb-item {'active' if active_tab_index == 1 else ''}">화이트리스트</a>
        </div>"""

    pattern = re.compile(r'<div class="breadcrumb".*?</div\s*>\s*<div class="page-title".*?</div\s*>\s*<div class="page-lnb".*?</div\s*>', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub(html_new, content)
    else:
        print(f"Could not find match in {filename}")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

process_file('maintenance.html', 0)
process_file('whitelist.html', 1)

print("Fixed styles in maintenance and whitelist to match exact LNB design.")
