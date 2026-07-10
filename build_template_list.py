import os

with open('notice.html', 'r', encoding='utf-8') as f:
    notice_html = f.read()

# Extract everything up to <div class="main-content">
base_parts = notice_html.split('<div class="main-content">')
base = base_parts[0] + '<div class="main-content">\n'

template_list_html = """
        <div class="breadcrumb">
            포털 관리 <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 공지 발송 <i class="fa-solid fa-chevron-right"></i> 템플릿 관리
        </div>

        <div class="list-header-bar">
            <div class="list-search">
                <span style="color: #94A3B8; margin-right: 10px;">(전체 : 3)</span>
                <select>
                    <option>템플릿 제목</option>
                </select>
                <input type="text" placeholder="검색어를 입력하세요">
                <button class="btn btn-primary">조회</button>
            </div>
            <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary" onclick="location.href='notice.html'">목록으로</button>
                <button class="btn btn-primary" onclick="alert('등록 화면 이동 (준비중)')">템플릿 등록</button>
            </div>
        </div>

        <table class="data-table">
            <thead>
                <tr>
                    <th>번호</th>
                    <th>템플릿 제목</th>
                    <th>사용 언어 수</th>
                    <th>등록일시</th>
                    <th>등록자</th>
                    <th>수정</th>
                    <th>기능</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>3</td>
                    <td>이벤트 당첨 안내 기본 템플릿</td>
                    <td>4개 (KO, EN, ZH-CN, TH)</td>
                    <td>2026-07-05 10:20:15</td>
                    <td>이주형</td>
                    <td><a href="#" style="color:#94A3B8;" onclick="alert('수정 화면 (준비중)')">수정</a></td>
                    <td>
                        <button class="btn-icon"><i class="fa-solid fa-chevron-up"></i></button>
                        <button class="btn-icon disabled"><i class="fa-solid fa-chevron-down"></i></button>
                        <button class="btn-icon"><i class="fa-solid fa-angles-up"></i></button>
                    </td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>정기 점검 안내 템플릿</td>
                    <td>전체 언어 (9개)</td>
                    <td>2026-06-15 14:11:00</td>
                    <td>이주형</td>
                    <td><a href="#" style="color:#94A3B8;" onclick="alert('수정 화면 (준비중)')">수정</a></td>
                    <td>
                        <button class="btn-icon"><i class="fa-solid fa-chevron-up"></i></button>
                        <button class="btn-icon"><i class="fa-solid fa-chevron-down"></i></button>
                        <button class="btn-icon"><i class="fa-solid fa-angles-up"></i></button>
                    </td>
                </tr>
                <tr>
                    <td>1</td>
                    <td>사전예약 리마인드 템플릿</td>
                    <td>전체 언어 (9개)</td>
                    <td>2026-06-01 09:00:00</td>
                    <td>이주형</td>
                    <td><a href="#" style="color:#94A3B8;" onclick="alert('수정 화면 (준비중)')">수정</a></td>
                    <td>
                        <button class="btn-icon"><i class="fa-solid fa-chevron-up"></i></button>
                        <button class="btn-icon"><i class="fa-solid fa-chevron-down"></i></button>
                        <button class="btn-icon"><i class="fa-solid fa-angles-up"></i></button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>
"""

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(base + template_list_html)

print("template.html built successfully.")
