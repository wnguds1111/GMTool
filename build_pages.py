import os
import re

# Read the current notice.html to extract the layout base
with open('notice.html', 'r', encoding='utf-8') as f:
    notice_content = f.read()

# Update sidebar to add 템플릿 관리
sidebar_find = """<li class="sub-nav-item" onclick="location.href='mail_individual.html'">개별 우편 발송</li>"""
sidebar_replace = """<li class="sub-nav-item" onclick="location.href='mail_individual.html'">개별 우편 발송</li>
                        <li class="sub-nav-item" onclick="location.href='template.html'">템플릿 관리</li>"""

def update_sidebar(html, active_page='notice.html'):
    html = html.replace(sidebar_find, sidebar_replace)
    # Reset all active states
    html = re.sub(r'<li class="sub-nav-item active"', r'<li class="sub-nav-item"', html)
    # Set the active page
    html = html.replace(f'<li class="sub-nav-item" onclick="location.href=\'{active_page}\'">', f'<li class="sub-nav-item active" onclick="location.href=\'{active_page}\'">')
    return html

# 10 mock items
mock_items = [
    (10, '일반', 'GetPoring 1.2 업데이트 안내', '2026-07-20 10:00:00 ~ 무기한', '2026-07-15 09:00:00', '문솔민', 'Y'),
    (9, '이벤트', '여름 맞이 수영복 스킨 획득 이벤트', '2026-07-18 12:00:00 ~ 2026-08-18 12:00:00', '2026-07-14 11:20:00', '이주형', 'Y'),
    (8, '점검', '7월 15일 임시 점검 완료 안내', '2026-07-15 14:00:00 ~ 2026-07-16 14:00:00', '2026-07-15 14:05:00', '이주형', 'N'),
    (7, '일반', '알려진 버그 안내 및 수정 일정', '2026-07-12 18:00:00 ~ 무기한', '2026-07-12 17:30:00', '이주형', 'Y'),
    (6, '점검', '7월 12일 정기 점검 안내', '2026-07-11 00:00:00 ~ 2026-07-12 12:00:00', '2026-07-08 14:11:00', '문솔민', 'N'),
    (5, '이벤트', '신규 가입 유저 달성 보상 이벤트', '2026-07-10 15:00:00 ~ 2026-08-10 15:00:00', '2026-07-09 10:20:15', '이주형', 'Y'),
    (4, '일반', 'GetPoring 사전예약 안내', '2026-07-10 15:00:00 ~ 무기한', '2026-07-09 10:20:15', '이주형', 'Y'),
    (3, '점검', '클라우드 서버 긴급 안정화 작업', '2026-07-05 02:00:00 ~ 2026-07-05 06:00:00', '2026-07-04 20:11:00', '문솔민', 'N'),
    (2, '일반', '사전예약 페이지 오픈 안내', '2026-07-01 10:00:00 ~ 무기한', '2026-07-01 09:30:00', '이주형', 'Y'),
    (1, '일반', 'GetPoring 커뮤니티 정책 안내', '2026-07-01 10:00:00 ~ 무기한', '2026-07-01 09:20:00', '문솔민', 'Y'),
]

tbody_content = ""
for item in mock_items:
    tbody_content += f"""                    <tr>
                        <td>{item[0]}</td>
                        <td>{item[1]}</td>
                        <td>{item[2]}</td>
                        <td>{item[3]}</td>
                        <td>{item[4]}</td>
                        <td>{item[5]}</td>
                        <td>{item[6]}</td>
                        <td><a href="#" style="color:#94A3B8;" onclick="location.href='notice_form.html?id={item[0]}'">수정</a></td>
                        <td>
                            <button class="btn-icon"><i class="fa-solid fa-chevron-up"></i></button>
                            <button class="btn-icon"><i class="fa-solid fa-chevron-down"></i></button>
                            <button class="btn-icon"><i class="fa-solid fa-angles-up"></i></button>
                        </td>
                    </tr>\n"""

# notice.html construction
notice_base = notice_content.split('<!-- List View -->')[0]

# remove script for toggling
notice_base = re.sub(r'<script>.*?</script>', '', notice_base, flags=re.DOTALL)

# update sidebar in notice_base
notice_base = update_sidebar(notice_base, 'notice.html')

list_view = """
        <!-- List View -->
        <div id="listView">
            <div class="breadcrumb">
                포털 관리 <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 공지 발송
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
                <button class="btn btn-primary" onclick="location.href='notice_form.html'">등록</button>
            </div>

            <table class="data-table">
                <thead>
                    <tr>
                        <th>번호</th>
                        <th>공지 구분</th>
                        <th>제목</th>
                        <th>노출기간</th>
                        <th>등록일시</th>
                        <th>등록자</th>
                        <th>게시 여부</th>
                        <th>수정</th>
                        <th>기능</th>
                    </tr>
                </thead>
                <tbody>
""" + tbody_content + """                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

with open('notice.html', 'w', encoding='utf-8') as f:
    f.write(notice_base + list_view)

# notice_form.html construction
form_view = notice_content.split('<!-- Form View -->')[1].split('</div>\n\n    </div>')[0]

# Update form display style to block and remove id/class
form_view = form_view.replace('id="formView" class="form-view"', '')

# Update buttons to navigate instead of toggleView
form_view = form_view.replace("toggleView('list')", "location.href='notice.html'")

# We need the base up to <div class="main-content">
notice_form_base = update_sidebar(notice_base, 'notice.html')
# Replace breadcrumb title for form
notice_form_html = notice_form_base + """
        <!-- Form View -->
        <div>
""" + form_view + """
        </div>
    </div>
    <script>
        // Tab click behavior
        document.querySelectorAll('.lang-tab').forEach(tab => {
            tab.addEventListener('click', function() {
                document.querySelectorAll('.lang-tab').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    </script>
</body>
</html>
"""

# ensure <style> doesn't hide .form-view since we removed the class, but just in case:
notice_form_html = notice_form_html.replace('.form-view { display: none; }', '')

with open('notice_form.html', 'w', encoding='utf-8') as f:
    f.write(notice_form_html)


# template.html construction (Stub)
template_base = update_sidebar(notice_base, 'template.html')
template_html = template_base + """
        <div class="breadcrumb">
            포털 관리 <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 템플릿 관리
        </div>

        <div class="page-title">템플릿 관리</div>

        <div style="padding: 40px; text-align: center; color: #94A3B8; font-size: 14px; border: 2px dashed #E2E8F0; border-radius: 8px; margin-top: 20px;">
            템플릿 관리 리스트 및 설정 화면 영역 (준비 중)
        </div>
    </div>
</body>
</html>
"""

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(template_html)

# Also update index.html to have the new sidebar
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

index_content = update_sidebar(index_content, 'index.html')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)
