import os
import re

# 1. Update mail_all_form.html dropdown
with open('mail_all_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_select_area = r'<select class="form-control" style="width: 300px;">.*?</select>\s*<div style="font-size: 13px; color: #64748B; margin-top: 8px;">.*?</div>'
new_select_area = """<select class="form-control" style="width: 300px;">
                        <option value="1">[1] Mailbox_01</option>
                        <option value="100">[100] Mailbox_02</option>
                        <option value="1000">[1000] Mailbox_03</option>
                        <option value="1001">[1001] Mailbox_04</option>
                        <option value="1002" selected>[1002] Mailbox_05</option>
                        <option value="2001">[2001] Mailbox_05</option>
                    </select>
                    <div style="font-size: 13px; color: #64748B; margin-top: 8px;">제목키 Mail_Reward_PreReg_Title · 본문키 Mail_Reward_PreReg_Desc · 유저 언어로 자동 현지화</div>"""

content = re.sub(old_select_area, new_select_area, content, flags=re.DOTALL)
with open('mail_all_form.html', 'w', encoding='utf-8') as f:
    f.write(content)


# 2. Update mail_template_form.html to be specialized for Mailbox Templates
with open('mail_template_form.html', 'r', encoding='utf-8') as f:
    tpl_content = f.read()

# Replace everything from <div class="form-group-title" style="margin-top:0;">기본 정보</div>
# down to <div class="form-actions">
start_idx = tpl_content.find('<div class="form-group-title" style="margin-top:0;">기본 정보</div>')
end_idx = tpl_content.find('<div class="form-actions">')

if start_idx != -1 and end_idx != -1:
    new_form_content = """<div class="form-group-title" style="margin-top:0;">기본 정보</div>
        <table class="form-table">
            <tr>
                <td class="label-cell">Mailbox ID</td>
                <td class="input-cell">
                    <input type="number" class="form-control short" value="1002">
                </td>
            </tr>
            <tr>
                <td class="label-cell">Mailbox 이름</td>
                <td class="input-cell">
                    <input type="text" class="form-control" value="Mailbox_05" placeholder="예: Mailbox_05">
                </td>
            </tr>
        </table>

        <div class="form-group-title">현지화 키 정보</div>
        <table class="form-table">
            <tr>
                <td class="label-cell">제목키 (Title Key)</td>
                <td class="input-cell">
                    <input type="text" class="form-control" value="Mail_Reward_PreReg_Title" placeholder="예: Mail_Reward_PreReg_Title">
                </td>
            </tr>
            <tr>
                <td class="label-cell">본문키 (Body Key)</td>
                <td class="input-cell">
                    <input type="text" class="form-control" value="Mail_Reward_PreReg_Desc" placeholder="예: Mail_Reward_PreReg_Desc">
                </td>
            </tr>
        </table>
        
        <div class="form-group-title">사용 정보</div>
        <table class="form-table">
            <tr>
                <td class="label-cell">사용 여부</td>
                <td class="input-cell">
                    <div class="radio-group">
                        <label class="radio-label"><input type="radio" name="publish" checked> 사용</label>
                        <label class="radio-label"><input type="radio" name="publish"> 미사용</label>
                    </div>
                </td>
            </tr>
        </table>
        
        """
    tpl_content = tpl_content[:start_idx] + new_form_content + tpl_content[end_idx:]
    
    # Also remove the script block at the bottom since language tabs are gone
    script_start = tpl_content.find('<script>')
    if script_start != -1:
        script_end = tpl_content.find('</script>', script_start)
        tpl_content = tpl_content[:script_start] + tpl_content[script_end + 9:]

    with open('mail_template_form.html', 'w', encoding='utf-8') as f:
        f.write(tpl_content)

print("Updated mail_all_form.html and mail_template_form.html")
