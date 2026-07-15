import os

with open('user_management.html', 'r', encoding='utf-8') as f:
    content = f.read()

# player_detail.html 내용 생성
# user_management.html은 1~514라인까지 Left Panel.
# 515: <!-- Main Content -->
head_nav = content[:content.find('<div class="main-content">') + len('<div class="main-content">')]

main_content_start = """
        <div class="breadcrumb" style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px; display: flex; align-items: center; gap: 12px;">
            WEB <i class="fa-solid fa-chevron-right" style="color: #CBD5E1; font-size: 14px;"></i> GetPoring <i class="fa-solid fa-chevron-right" style="color: #CBD5E1; font-size: 14px;"></i> <span style="cursor: pointer;" onclick="location.href='user_management.html'">게임 유저 관리</span> <i class="fa-solid fa-chevron-right" style="color: #CBD5E1; font-size: 14px;"></i> 플레이어 상세
        </div>

        <div class="page-title" style="font-size: 24px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px;">
            플레이어 상세 — 36690843045728256 (Shard 1)
        </div>
"""

# 모달 body 내용 추출
modal_start_idx = content.find('<div class="modal-body">')
modal_end_idx = content.find('<!-- Tab 4: 결제 -->')
modal_end_idx = content.find('</div>\n                    </div>\n\n                </div>', modal_end_idx)

modal_body_content = content[modal_start_idx + len('<div class="modal-body">') : modal_end_idx + len('</div>\n                    </div>')]

# player_detail.html 조립
player_detail_html = head_nav + main_content_start + modal_body_content + """
    </div>
    <script>
    function switchDetailTab(element, tabId) {
        document.querySelectorAll('.page-lnb-item').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        
        element.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    }
    </script>
</body>
</html>
"""

player_detail_html = player_detail_html.replace('padding-top: 16px; background: white;', 'padding-top: 0; background: var(--main-bg);')

with open('player_detail.html', 'w', encoding='utf-8') as f:
    f.write(player_detail_html)

# user_management.html 수정
new_content = content.replace("openModal('playerDetailsModal')", "location.href='player_detail.html'")

# 모달 제거
modal_full_start = new_content.find('<!-- Player Details Modal -->')
script_start = new_content.find('<script>', modal_full_start)
new_content = new_content[:modal_full_start] + new_content[script_start:]

# switchDetailTab 함수 제거
func_start = new_content.find('function switchDetailTab')
if func_start != -1:
    func_end = new_content.find('}\n        function openModal', func_start)
    new_content = new_content[:func_start] + new_content[func_end + 2:]

with open('user_management.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("success")
