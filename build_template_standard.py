import os

with open('notice.html', 'r', encoding='utf-8') as f:
    notice_html = f.read()

base_parts = notice_html.split('<div class="main-content">')
base = base_parts[0] + '<div class="main-content">\n'

# We need the language card CSS since notice.html doesn't have it.
lang_css = """
    <style>
        .lang-card {
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: #FFFFFF;
        }
        
        .lang-card-header {
            display: flex;
            align-items: center;
            font-size: 14px;
            font-weight: 700;
            color: #475569;
            margin-bottom: 12px;
        }
        
        .lang-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .lang-dot.red { background-color: #EF4444; }
        .lang-dot.gray { background-color: #CBD5E1; }
        
        .lang-req { color: #EF4444; margin-left: 4px; }
        
        .help-text {
            font-size: 13px;
            color: #64748B;
            margin-bottom: 16px;
            font-weight: 500;
        }
    </style>
"""

# Insert lang_css into base
head_split = base.split('</head>')
base = head_split[0] + lang_css + '</head>' + head_split[1]

# 1. template.html (List view)
template_list_html = """
        <div class="breadcrumb">
            포털 관리 <i class="fa-solid fa-chevron-right"></i> GetPoring <i class="fa-solid fa-chevron-right"></i> 공지 발송 <i class="fa-solid fa-chevron-right"></i> 템플릿 관리
        </div>

        <div class="list-header-bar">
            <div class="list-search">
                <span style="color: #94A3B8; margin-right: 10px;">(전체 : 3)</span>
                <select>
                    <option>템플릿 이름</option>
                </select>
                <input type="text" placeholder="검색어를 입력하세요">
                <button class="btn btn-primary">조회</button>
            </div>
            <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary" onclick="location.href='notice.html'">공지로 돌아가기</button>
                <button class="btn btn-primary" onclick="location.href='template_form.html'">새 템플릿</button>
            </div>
        </div>

        <table class="data-table">
            <thead>
                <tr>
                    <th>번호</th>
                    <th>템플릿 이름</th>
                    <th>유형</th>
                    <th>수정일</th>
                    <th>관리</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>3</td>
                    <td style="font-weight: 600;">test</td>
                    <td>일반</td>
                    <td>2026. 7. 10. 오전 10:50:45</td>
                    <td>
                        <button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='template_form.html'">수정</button>
                        <button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>
                    </td>
                </tr>
                <tr>
                    <td>2</td>
                    <td style="font-weight: 600;">정기 점검 템플릿</td>
                    <td>점검</td>
                    <td>2026. 7. 9. 오후 02:15:22</td>
                    <td>
                        <button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='template_form.html'">수정</button>
                        <button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>
                    </td>
                </tr>
                <tr>
                    <td>1</td>
                    <td style="font-weight: 600;">여름 이벤트 당첨자</td>
                    <td>이벤트</td>
                    <td>2026. 7. 8. 오전 11:30:00</td>
                    <td>
                        <button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='template_form.html'">수정</button>
                        <button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>
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

# 2. template_form.html (Form view)
template_form_html = """
        <div class="form-header-bar">
            <button class="btn btn-secondary" onclick="location.href='template.html'">뒤로가기</button>
        </div>
        
        <div class="form-section-title">템플릿 등록/수정</div>
        
        <div class="form-group-title" style="margin-top:0;">기본 정보</div>
        <table class="form-table">
            <tr>
                <td class="label-cell">템플릿 이름</td>
                <td class="input-cell">
                    <input type="text" class="form-control" value="test">
                </td>
            </tr>
            <tr>
                <td class="label-cell">유형</td>
                <td class="input-cell">
                    <select class="form-control short">
                        <option value="1" selected>일반</option>
                        <option value="2">점검</option>
                        <option value="3">이벤트</option>
                    </select>
                </td>
            </tr>
        </table>

        <div class="form-group-title">언어별 정보</div>
        <div class="help-text">언어별 제목·본문 — 기본 언어(한국어) 본문 필수, 작성된 언어만 게임에 노출</div>
        
        <div class="lang-card">
            <div class="lang-card-header">
                <div class="lang-dot red"></div> 한국어 <span class="lang-req">*</span>
            </div>
            <input type="text" class="form-control" placeholder="제목" value="테스트 공지입니다." style="margin-bottom: 8px;">
            <textarea class="form-control" placeholder="본문" style="height: 100px; resize: vertical;">테스트 공지 내용입니다.</textarea>
        </div>
        
        <div class="lang-card">
            <div class="lang-card-header">
                <div class="lang-dot gray"></div> English
            </div>
            <input type="text" class="form-control" placeholder="제목" style="margin-bottom: 8px;">
            <textarea class="form-control" placeholder="본문" style="height: 100px; resize: vertical;"></textarea>
        </div>
        
        <div class="lang-card">
            <div class="lang-card-header">
                <div class="lang-dot gray"></div> 日本語
            </div>
            <input type="text" class="form-control" placeholder="제목" style="margin-bottom: 8px;">
            <textarea class="form-control" placeholder="본문" style="height: 100px; resize: vertical;"></textarea>
        </div>
        
        <div class="lang-card">
            <div class="lang-card-header">
                <div class="lang-dot gray"></div> Español (ES)
            </div>
            <input type="text" class="form-control" placeholder="제목" style="margin-bottom: 8px;">
            <textarea class="form-control" placeholder="본문" style="height: 100px; resize: vertical;"></textarea>
        </div>

        <div class="form-actions">
            <button class="btn btn-secondary" onclick="location.href='template.html'">취소</button>
            <button class="btn btn-primary" onclick="alert('등록되었습니다.'); location.href='template.html'">저장</button>
        </div>
    </div>
</body>
</html>
"""

with open('template_form.html', 'w', encoding='utf-8') as f:
    f.write(base + template_form_html)
