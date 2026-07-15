import os
import re

with open('mail_all.html', 'r', encoding='utf-8') as f:
    content = f.read()

rows_all = ""
titles = ["점검 보상 지급 안내", "여름 이벤트 보상", "신규 가입 환영 패키지", "서버 렉 보상", "푸시 알림 보상", "주말 핫타임 보상", "버그 수정 완료 보상", "게릴라 이벤트 당첨", "1주년 기념 선물", "사전예약 100만 달성"]

for i in range(10):
    applied = i % 2 != 0  # odd index -> applied, even index -> not applied
    expire_text = "기본" if i % 3 == 0 else "2026-08-01 12:00:00"
    
    if applied:
        # User said "1/1 이건 필요없어", meaning we don't need the 1/1 text.
        # Let's just make it already in the '게임서버 적용' state, or make all of them '샤드 적용'.
        # I'll make the applied ones '게임서버 적용' with the primary style.
        shard_html = f"""<div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                            <button class="btn" style="padding: 2px 10px; font-size: 13px; background-color: #16A34A; color: white; border: 1px solid #16A34A; cursor: not-allowed;" disabled>적용 완료</button>
                        </div>"""
    else:
        # Button on the left without 0/0. With onClick confirm.
        shard_html = f"""<div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                            <button class="btn btn-outline" style="padding: 2px 10px; font-size: 13px;" onclick="applyShard(this)">게임서버 적용</button>
                        </div>"""
    
    # Manage is always '상세'
    manage_html = """<button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='mail_all_detail.html'">상세</button>"""

    rows_all += f"""
                <tr>
                    <td style="font-weight: 600;">{titles[i]}</td>
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

# Add script if not exists
script_code = """
    <script>
        function applyShard(btn) {
            if (confirm("게임서버에 적용하시겠습니까?")) {
                btn.innerText = "적용 완료";
                btn.className = "btn";
                btn.style.backgroundColor = "#16A34A";
                btn.style.color = "white";
                btn.style.borderColor = "#16A34A";
                btn.style.cursor = "not-allowed";
                btn.disabled = true;
            }
        }
    </script>
</body>"""

if "function applyShard" not in content:
    content = content.replace("</body>", script_code)

with open('mail_all.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated mail_all.html with applyShard logic and removed 1/1 and 0/0.")
