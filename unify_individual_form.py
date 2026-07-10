import os
import re

with open('mail_all_form.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# 1. Update LNB active state
base_html = base_html.replace('<a href="mail_all.html" class="page-lnb-item active">전체 우편 발송</a>', '<a href="mail_all.html" class="page-lnb-item">전체 우편 발송</a>')
base_html = base_html.replace('<a href="mail_individual.html" class="page-lnb-item">개별 우편 발송</a>', '<a href="mail_individual.html" class="page-lnb-item active">개별 우편 발송</a>')

# 2. Breadcrumbs
base_html = base_html.replace('우편 관리 <i class="fa-solid fa-chevron-right"></i> 전체 우편 작성', '우편 관리 <i class="fa-solid fa-chevron-right"></i> 개별 우편 작성')

# 3. Header Texts and Close Button
base_html = base_html.replace('<div style="font-size: 20px; font-weight: 700; margin-bottom: 8px;">전체 우편 작성</div>', '<div style="font-size: 20px; font-weight: 700; margin-bottom: 8px;">단건 우편 작성</div>')
base_html = base_html.replace('<div style="font-size: 15px; color: #64748B;">중앙 등록 후 목록에서 \'샤드 적용\'을 실행하세요.</div>', '<div style="font-size: 15px; color: #64748B;">특정 플레이어에게 직접 발송 (ShardID는 PlayerID에서 자동 계산)</div>')
# This replaces the onclick for X button and 취소/등록 buttons
base_html = base_html.replace("location.href='mail_all.html'", "location.href='mail_individual.html'")

# 4. Insert PlayerID Row
player_row = """
            <tr>
                <td class="label-cell">PlayerID / ShardID</td>
                <td class="input-cell">
                    <div style="display: flex; gap: 16px; align-items: center;">
                        <input type="text" class="form-control" style="width: 300px;" placeholder="PlayerID 입력">
                        <span style="font-size: 14px; font-weight: 600; color: var(--text-dark);">ShardID (자동)</span>
                        <input type="text" class="form-control" style="width: 150px; background-color: #F8FAFC;" value="-" readonly>
                    </div>
                </td>
            </tr>"""

# Insert right after <table class="form-table">
base_html = base_html.replace('<table class="form-table">', '<table class="form-table">\n' + player_row)

# 5. Change 등록 to 발송 for the main action button
base_html = base_html.replace('>등록</button>', '>발송</button>')

with open('mail_individual_form.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

print("Unified mail_individual_form.html to match mail_all_form.html style")
