import re

with open('mail_all.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace '샤드 적용' button and remove '0/0'
# Target pattern: <button class="btn btn-outline" style="padding: 2px 10px; font-size: 13px;" onclick="document.getElementById('shardModal').style.display='flex'">샤드 적용</button>\s*<span>0/0</span>
content = re.sub(
    r'<button([^>]*?)>샤드 적용</button>\s*<span>0/0</span>',
    r'<button\1>게임서버 적용</button>',
    content
)

# 2. Replace '수정' and '삭제' with '상세'
# Target pattern: <button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href='mail_all_form.html'">수정</button>\s*<button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>
content = re.sub(
    r'<button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href=\'mail_all_form.html\'">수정</button>\s*<button class="btn btn-outline" style="padding: 4px 12px;">삭제</button>',
    r'<button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href=\'mail_all_detail.html\'">상세</button>',
    content
)

# 3. Optional: replace '-' with '상세' as well so every row has it
content = re.sub(
    r'<span style="color: #94A3B8; font-size: 14px;">-</span>',
    r'<button class="btn btn-outline" style="padding: 4px 12px;" onclick="location.href=\'mail_all_detail.html\'">상세</button>',
    content
)

with open('mail_all.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated mail_all.html")
