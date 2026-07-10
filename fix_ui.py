import os

files = ['index.html', 'notice.html', 'notice_form.html', 'template.html']

for f in files:
    if not os.path.exists(f):
        continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Remove 템플릿 관리 from sidebar
    content = content.replace("""<li class="sub-nav-item" onclick="location.href='template.html'">템플릿 관리</li>""", "")
    content = content.replace("""<li class="sub-nav-item active" onclick="location.href='template.html'">템플릿 관리</li>""", "")
    
    # Clean up empty lines left behind if any
    lines = content.split('\n')
    cleaned_lines = [line for line in lines if line.strip() != '']
    content = '\n'.join(cleaned_lines)
    
    # 2. Change author '문솔민' to '이주형'
    content = content.replace("<td>문솔민</td>", "<td>이주형</td>")
    
    # 3. In notice.html, add template management button next to register button
    if f == 'notice.html':
        target_buttons_old = """                <button class="btn btn-primary" onclick="location.href='notice_form.html'">등록</button>"""
        target_buttons_new = """                <div style="display: flex; gap: 8px;">
                    <button class="btn btn-outline" onclick="location.href='template.html'">템플릿 관리</button>
                    <button class="btn btn-primary" onclick="location.href='notice_form.html'">등록</button>
                </div>"""
        content = content.replace(target_buttons_old, target_buttons_new)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("UI fixed successfully.")
