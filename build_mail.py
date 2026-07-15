import os
import shutil

# 1. Update mail_all.html List View
with open('mail_all.html', 'r', encoding='utf-8') as f:
    mail_all_content = f.read()

list_ui = """
        <div class="list-header-bar" style="margin-top: 10px; align-items: flex-start; flex-direction: column;">
            <div style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px;">전체 우편</div>
            <div style="font-size: 15px; color: #64748B; margin-bottom: 16px;">AccountDB 중앙 등록 후 게임 샤드에 적용</div>
            <button class="btn btn-primary" onclick="location.href='mail_all_form.html'">전체 우편 작성</button>
        </div>

        <table class="data-table" style="margin-top: 24px;">
            <thead>
                <tr>
                    <th>제목</th>
                    <th>종류</th>
                    <th>만료</th>
                    <th>적용(샤드)</th>
                    <th>작성자</th>
                    <th>관리</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="6" style="padding: 60px 0; color: #94A3B8;">등록된 전체 우편이 없습니다.</td>
                </tr>
            </tbody>
        </table>
"""

# Replace the preparation content with the new list UI
import re
new_mail_all_content = re.sub(
    r'<div class="page-title">전체 우편 발송</div>.*?</div>\s*</div>\s*</body>',
    list_ui + '\n    </div>\n</body>',
    mail_all_content,
    flags=re.DOTALL
)

with open('mail_all.html', 'w', encoding='utf-8') as f:
    f.write(new_mail_all_content)

# 2. Create mail_all_form.html based on template.html/notice.html layout
with open('notice.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Extract everything up to <div class="main-content">
base_parts = base_html.split('<div class="main-content">')
top_html = base_parts[0]

# Change active sidebar state to mail_all.html
top_html = top_html.replace('<li class="sub-nav-item active" onclick="location.href=\'notice.html\'">공지 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'notice.html\'">공지 관리</li>')
top_html = top_html.replace('<li class="sub-nav-item" onclick="location.href=\'mail_all.html\'">우편 관리</li>', '<li class="sub-nav-item active" onclick="location.href=\'mail_all.html\'">우편 관리</li>')

form_html = """
    <div class="main-content">
        <div class="breadcrumb">
            WEB <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 우편 관리 <i class="fa-solid fa-chevron-right"></i> 전체 우편 작성
        </div>

        <div class="page-lnb">
            <a href="mail_all.html" class="page-lnb-item active">전체 우편 발송</a>
            <a href="mail_individual.html" class="page-lnb-item">개별 우편 발송</a>
        </div>

        <div class="form-header-bar" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
            <div>
                <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px;">전체 우편 작성</div>
                <div style="font-size: 15px; color: #64748B;">중앙 등록 후 목록에서 '샤드 적용'을 실행하세요.</div>
            </div>
            <i class="fa-solid fa-xmark" style="font-size: 24px; color: #94A3B8; cursor: pointer;" onclick="location.href='mail_all.html'"></i>
        </div>

        <table class="form-table">
            <tr>
                <td class="label-cell">발송 방식</td>
                <td class="input-cell">
                    <div style="display: flex; gap: 8px;">
                        <button class="btn btn-primary" id="btn-free" onclick="toggleMode('free')">자유 텍스트</button>
                        <button class="btn btn-outline" id="btn-template" onclick="toggleMode('template')">등록 템플릿</button>
                    </div>
                </td>
            </tr>
            <tr id="row-template" style="display: none;">
                <td class="label-cell">등록 우편 (Mailbox)</td>
                <td class="input-cell">
                    <select class="form-control" style="width: 300px;">
                        <option>템플릿 선택</option>
                        <option>[1] Mailbox_01</option>
                        <option>[100] Mailbox_02</option>
                    </select>
                </td>
            </tr>
            <tr id="row-title">
                <td class="label-cell">제목</td>
                <td class="input-cell">
                    <input type="text" class="form-control" placeholder="제목을 입력하세요">
                </td>
            </tr>
            <tr id="row-body">
                <td class="label-cell">본문</td>
                <td class="input-cell">
                    <textarea class="form-control" placeholder="본문 내용을 입력하세요"></textarea>
                </td>
            </tr>
            <tr>
                <td class="label-cell">만료일</td>
                <td class="input-cell">
                    <input type="datetime-local" class="form-control" style="width: 250px;">
                </td>
            </tr>
            <tr>
                <td class="label-cell">보상</td>
                <td class="input-cell">
                    <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px;">
                        <input type="text" class="form-control" style="width: 300px;" placeholder="아이템 검색 / ID">
                        <input type="number" class="form-control" style="width: 100px;" placeholder="수량">
                        <button class="btn btn-outline">삭제</button>
                    </div>
                    <button class="btn btn-outline">보상 추가</button>
                </td>
            </tr>
        </table>

        <div class="form-actions" style="justify-content: flex-end; gap: 12px; margin-top: 24px;">
            <button class="btn btn-outline" style="padding: 10px 24px;" onclick="location.href='mail_all.html'">취소</button>
            <button class="btn btn-primary" style="padding: 10px 24px;" onclick="location.href='mail_all.html'">등록</button>
        </div>
    </div>
    
    <script>
        function toggleMode(mode) {
            const btnFree = document.getElementById('btn-free');
            const btnTemplate = document.getElementById('btn-template');
            const rowTemplate = document.getElementById('row-template');
            const rowTitle = document.getElementById('row-title');
            const rowBody = document.getElementById('row-body');
            
            if (mode === 'free') {
                btnFree.className = 'btn btn-primary';
                btnTemplate.className = 'btn btn-outline';
                rowTemplate.style.display = 'none';
                rowTitle.style.display = 'table-row';
                rowBody.style.display = 'table-row';
            } else {
                btnFree.className = 'btn btn-outline';
                btnTemplate.className = 'btn btn-primary';
                rowTemplate.style.display = 'table-row';
                rowTitle.style.display = 'none';
                rowBody.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

with open('mail_all_form.html', 'w', encoding='utf-8') as f:
    f.write(top_html + form_html)

print("Created mail_all.html and mail_all_form.html successfully.")
