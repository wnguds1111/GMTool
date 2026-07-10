import os
import re

with open('mail_all.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Generate new rows for mail_all.html
rows_all = ""
titles = ["점검 보상 지급 안내", "여름 이벤트 보상", "신규 가입 환영 패키지", "서버 렉 보상", "푸시 알림 보상", "주말 핫타임 보상", "버그 수정 완료 보상", "게릴라 이벤트 당첨", "1주년 기념 선물", "사전예약 100만 달성"]

for i in range(10):
    applied = i % 2 != 0  # odd index -> applied (1/1), even index -> not applied (0/0)
    shard_text = "1/1" if applied else "0/0"
    expire_text = "기본" if i % 3 == 0 else "2026-08-01 12:00:00"
    
    if applied:
        shard_html = f"<div>{shard_text}</div>"
        manage_html = """<span style="color: #94A3B8; font-size: 14px;">-</span>"""
    else:
        shard_html = f"""<div>{shard_text}</div>
                        <button class="btn btn-outline" style="padding: 2px 10px; font-size: 13px; margin-top: 6px;">샤드 적용</button>"""
        manage_html = """<button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='mail_all_form.html'">수정</button>
                        <button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>"""

    rows_all += f"""
                <tr>
                    <td style="font-weight: 600; text-align: left; padding-left: 16px;">{titles[i]}</td>
                    <td>Reward</td>
                    <td>{expire_text}</td>
                    <td>{shard_html}
                    </td>
                    <td>이주형</td>
                    <td>
                        {manage_html}
                    </td>
                </tr>
"""

# Replace the tbody content
content = re.sub(r'<tbody>.*?</tbody>', f'<tbody>\n{rows_all}            </tbody>', content, flags=re.DOTALL)

with open('mail_all.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated mail_all.html table with Shard Apply button moved.")
