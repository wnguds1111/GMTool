import os
import re

# 1. Update mail_individual.html
with open('mail_individual.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the button
content = content.replace('<button class="btn btn-primary">개별 우편 작성</button>', '<button class="btn btn-primary" onclick="location.href=\'mail_individual_form.html\'">개별 우편 작성</button>')

with open('mail_individual.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Create mail_individual_form.html from mail_all_form.html (just to get the header/sidebar)
with open('mail_all_form.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Replace the active LNB
base_html = base_html.replace('<a href="mail_all.html" class="page-lnb-item active">전체 우편 발송</a>', '<a href="mail_all.html" class="page-lnb-item">전체 우편 발송</a>')
base_html = base_html.replace('<a href="mail_individual.html" class="page-lnb-item">개별 우편 발송</a>', '<a href="mail_individual.html" class="page-lnb-item active">개별 우편 발송</a>')

# Replace Breadcrumb
base_html = base_html.replace('우편 관리 <i class="fa-solid fa-chevron-right"></i> 전체 우편 작성', '우편 관리 <i class="fa-solid fa-chevron-right"></i> 개별 우편 작성')

# Remove the form-header-bar and form-table and form-actions
start_idx = base_html.find('<div class="form-header-bar"')
end_idx = base_html.find('</div>\n    \n    <script>')

if start_idx != -1 and end_idx != -1:
    stacked_form_html = """
        <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
            <div></div>
            <i class="fa-solid fa-xmark" style="font-size: 24px; color: #94A3B8; cursor: pointer;" onclick="location.href='mail_individual.html'"></i>
        </div>

        <div style="border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; background: var(--white); margin-bottom: 40px;">
            <div style="font-size: 16px; font-weight: 700; margin-bottom: 4px; color: var(--text-dark);">단건 우편</div>
            <div style="font-size: 13px; color: #64748B; margin-bottom: 24px;">특정 플레이어에게 직접 발송 (ShardID는 PlayerID에서 자동 계산)</div>
            
            <!-- PlayerID and ShardID -->
            <div style="display: flex; gap: 16px; margin-bottom: 16px;">
                <div style="flex: 1;">
                    <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">PlayerID</div>
                    <input type="text" class="form-control">
                </div>
                <div style="width: 200px;">
                    <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">ShardID (자동)</div>
                    <input type="text" class="form-control" value="-" readonly style="background-color: #F8FAFC;">
                </div>
            </div>

            <!-- 발송 방식 -->
            <div style="margin-bottom: 16px;">
                <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">발송 방식</div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn btn-primary" id="btn-free" onclick="toggleMode('free')" style="padding: 6px 12px; font-size: 13px;">자유 텍스트</button>
                    <button class="btn btn-outline" id="btn-template" onclick="toggleMode('template')" style="padding: 6px 12px; font-size: 13px;">등록 템플릿</button>
                </div>
            </div>

            <!-- 등록 템플릿 -->
            <div id="row-template" style="display: none; margin-bottom: 16px;">
                <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">등록 우편 (Mailbox)</div>
                <select class="form-control" style="width: 100%;">
                    <option value="1">[1] Mailbox_01</option>
                    <option value="100">[100] Mailbox_02</option>
                    <option value="1000">[1000] Mailbox_03</option>
                    <option value="1001">[1001] Mailbox_04</option>
                    <option value="1002" selected>[1002] Mailbox_05</option>
                    <option value="2001">[2001] Mailbox_05</option>
                </select>
                <div style="font-size: 13px; color: #64748B; margin-top: 8px;">제목키 Mail_Reward_PreReg_Title · 본문키 Mail_Reward_PreReg_Desc · 유저 언어로 자동 현지화</div>
            </div>
            
            <!-- 제목 -->
            <div id="row-title" style="margin-bottom: 16px;">
                <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">제목</div>
                <input type="text" class="form-control">
            </div>

            <!-- 본문 -->
            <div id="row-body" style="margin-bottom: 16px;">
                <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">본문</div>
                <textarea class="form-control" style="min-height: 100px;"></textarea>
            </div>

            <!-- 만료일 -->
            <div style="margin-bottom: 16px;">
                <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">만료일 (UTC, 필수)</div>
                <input type="datetime-local" class="form-control" style="width: 100%;">
            </div>

            <!-- 보상 -->
            <div style="margin-bottom: 24px;">
                <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">보상</div>
                <div class="reward-row" style="margin-bottom: 8px;">
                    <div class="reward-input-wrap" style="flex: 1; width: auto;">
                        <input type="text" class="form-control" value="1 Paid_Zeny" readonly style="border-color: var(--admin-tools-blue); box-shadow: 0 0 0 1px var(--admin-tools-blue);">
                        <span class="badge paid">유료</span>
                    </div>
                    <input type="text" class="form-control" style="width: 100px;" placeholder="수량">
                    <button class="btn btn-outline" style="padding: 8px 16px;">삭제</button>
                </div>
                <div class="reward-row" style="margin-bottom: 8px;">
                    <div class="reward-input-wrap" style="flex: 1; width: auto;">
                        <input type="text" class="form-control" value="1 Paid_Zeny" readonly style="border-color: var(--admin-tools-blue); box-shadow: 0 0 0 1px var(--admin-tools-blue);">
                        <span class="badge paid">유료</span>
                    </div>
                    <input type="text" class="form-control" style="width: 100px;" placeholder="수량">
                    <button class="btn btn-outline" style="padding: 8px 16px;">삭제</button>
                </div>
                <button class="btn btn-outline" style="padding: 6px 12px; font-size: 13px; margin-top: 4px;">보상 추가</button>
            </div>

            <!-- 발송 버튼 -->
            <div>
                <button class="btn btn-primary" style="padding: 8px 24px; font-weight: 600;" onclick="location.href='mail_individual.html'">발송</button>
            </div>
        </div>
"""
    base_html = base_html[:start_idx] + stacked_form_html + base_html[end_idx:]

with open('mail_individual_form.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

print("Created mail_individual_form.html and wired up the button.")
