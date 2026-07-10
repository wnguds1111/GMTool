import os
import re

# 1. Update mail_all_form.html (Rewards UI + Buttons)
with open('mail_all_form.html', 'r', encoding='utf-8') as f:
    form_html = f.read()

# Fix form-actions buttons to be space-between (취소 left, 등록 right)
form_html = form_html.replace(
    '<div class="form-actions" style="justify-content: flex-end; gap: 12px; margin-top: 24px;">',
    '<div class="form-actions" style="justify-content: space-between; margin-top: 24px;">'
)

# Insert CSS for badges
css_badge = """
        .reward-row { display: flex; gap: 8px; align-items: center; margin-bottom: 12px; }
        .reward-input-wrap { position: relative; width: 300px; display: flex; align-items: center; }
        .reward-input-wrap input { width: 100%; padding-right: 50px; }
        .badge { position: absolute; right: 8px; font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: 700; }
        .badge.free { background-color: #DCFCE7; color: #16A34A; }
        .badge.paid { background-color: #FEF3C7; color: #D97706; }
"""
if '.reward-row' not in form_html:
    form_html = form_html.replace('</style>', css_badge + '\n    </style>')

# Replace Rewards UI
old_rewards_ui = """<div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px;">
                        <input type="text" class="form-control" style="width: 300px;" placeholder="아이템 검색 / ID">
                        <input type="number" class="form-control" style="width: 100px;" placeholder="수량">
                        <button class="btn btn-outline">삭제</button>
                    </div>
                    <button class="btn btn-outline">보상 추가</button>"""

new_rewards_ui = """<div class="reward-row">
                        <div class="reward-input-wrap">
                            <input type="text" class="form-control" value="2 Free_Zeny" readonly>
                            <span class="badge free">무료</span>
                        </div>
                        <input type="text" class="form-control" style="width: 100px; text-align: right;" value="1,000">
                        <button class="btn btn-outline">삭제</button>
                    </div>
                    <div class="reward-row">
                        <div class="reward-input-wrap">
                            <input type="text" class="form-control" value="3 Paid_Dia" readonly>
                            <span class="badge paid">유료</span>
                        </div>
                        <input type="text" class="form-control" style="width: 100px; text-align: right;" value="500">
                        <button class="btn btn-outline">삭제</button>
                    </div>
                    <div class="reward-row">
                        <div class="reward-input-wrap">
                            <input type="text" class="form-control" placeholder="아이템 검색 / ID">
                        </div>
                        <input type="number" class="form-control" style="width: 100px;" placeholder="수량">
                        <button class="btn btn-outline">삭제</button>
                    </div>
                    <button class="btn btn-outline" style="margin-top: 4px;">보상 추가</button>"""

form_html = form_html.replace(old_rewards_ui, new_rewards_ui)

with open('mail_all_form.html', 'w', encoding='utf-8') as f:
    f.write(form_html)


# 2. Update mail_all.html (Add 10 sample rows)
with open('mail_all.html', 'r', encoding='utf-8') as f:
    mail_all_html = f.read()

rows_all = ""
titles = ["점검 보상 지급 안내", "여름 이벤트 보상", "신규 가입 환영 패키지", "서버 렉 보상", "푸시 알림 보상", "주말 핫타임 보상", "버그 수정 완료 보상", "게릴라 이벤트 당첨", "1주년 기념 선물", "사전예약 100만 달성"]
for i in range(10):
    rows_all += f"""
                <tr>
                    <td style="font-weight: 600;">{titles[i]}</td>
                    <td>{'점검' if i in [0,3,6] else '이벤트'}</td>
                    <td>2026-08-01 12:00:00</td>
                    <td>전체 샤드</td>
                    <td>이주형</td>
                    <td>
                        <button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='mail_all_form.html'">수정</button>
                        <button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>
                    </td>
                </tr>
"""

mail_all_html = re.sub(r'<tbody>.*?</tbody>', f'<tbody>\n{rows_all}            </tbody>', mail_all_html, flags=re.DOTALL)
with open('mail_all.html', 'w', encoding='utf-8') as f:
    f.write(mail_all_html)


# 3. Update mail_individual.html (Build UI and add 10 rows)
with open('mail_individual.html', 'r', encoding='utf-8') as f:
    mail_ind_html = f.read()

# It currently has <div class="page-title">개별 우편 발송</div> and <div ...>콘텐츠 영역 (준비 중)</div>
rows_ind = ""
ids = ["user_abcd123", "gnjoy_12049", "test_account99", "gravity_master", "player_001", "player_002", "player_003", "vip_user_777", "gnjoy_88412", "newbie_221"]
for i in range(10):
    rows_ind += f"""
                <tr>
                    <td style="font-weight: 600;">개별 문의 복구 아이템 지급</td>
                    <td>{ids[i]}</td>
                    <td>2026-08-15 00:00:00</td>
                    <td>이주형</td>
                    <td>
                        <button class="btn btn-outline" style="padding: 4px 12px;">수정</button>
                        <button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>
                    </td>
                </tr>
"""

ind_ui = f"""
        <div class="list-header-bar" style="margin-top: 10px; align-items: flex-start; flex-direction: column;">
            <div style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 6px;">개별 우편</div>
            <div style="font-size: 15px; color: #64748B; margin-bottom: 16px;">AccountDB 사용자 계정 단위로 개별 발송</div>
            <button class="btn btn-primary">개별 우편 작성</button>
        </div>

        <table class="data-table" style="margin-top: 24px;">
            <thead>
                <tr>
                    <th>제목</th>
                    <th>수신자(계정ID)</th>
                    <th>만료</th>
                    <th>작성자</th>
                    <th>관리</th>
                </tr>
            </thead>
            <tbody>
{rows_ind}            </tbody>
        </table>
"""

mail_ind_html = re.sub(
    r'<div class="page-title">개별 우편 발송</div>.*?</div>\s*</div>\s*</body>',
    ind_ui + '\n    </div>\n</body>',
    mail_ind_html,
    flags=re.DOTALL
)

with open('mail_individual.html', 'w', encoding='utf-8') as f:
    f.write(mail_ind_html)

print("Updated rewards UI, added sample data, and aligned buttons.")
