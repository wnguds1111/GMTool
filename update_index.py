import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove left-panel
start_idx = content.find('<div class="left-panel">')
end_idx = content.find('<!-- Main Content -->')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# Remove main-content rounded corners and shadow since it's now full screen
content = content.replace('<div class="main-content" style="background-color: #F8FAFC;">', '<div class="main-content" style="background-color: #F8FAFC; border-radius: 0; box-shadow: none;">')

# 2. Update Q&A section
new_qna = """<div class="dash-card" style="grid-column: 1 / -1; background: var(--white); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                <div class="dash-title" style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 20px; display: flex; align-items: center; gap: 8px;">
                    <i class="fa-solid fa-circle-question" style="color: var(--admin-tools-blue);"></i> 주요 질의 사항 (API 수급 필요 리스트)
                </div>
                
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 16px; border-left: 4px solid var(--admin-tools-blue);">
                        <div style="font-weight: 700; color: var(--text-dark); font-size: 15px;">1. 우편 관리 > 등록 템플릿 > 조회 API 수급 필요</div>
                    </div>
                    
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 16px; border-left: 4px solid var(--admin-tools-blue);">
                        <div style="font-weight: 700; color: var(--text-dark); font-size: 15px;">2. 단건 우편 발송의 건 이력 조회 API 수급 필요</div>
                    </div>
                </div>
            </div>"""

qna_start = content.find('<!-- 질의 사항 -->')
qna_end = content.find('</div>\n\n        </div>')

if qna_start != -1 and qna_end != -1:
    content = content[:qna_start] + '<!-- 질의 사항 -->\n            ' + new_qna + '\n\n' + content[qna_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html: Removed left menu and updated Q&A list.")
