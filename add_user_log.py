import os
import re

# 1. Read a base file to get the layout
with open('prereg.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# 2. Extract template parts
start_main = base_html.find('<div class="main-content">')
end_main = base_html.find('</body>')

template_prefix = base_html[:start_main]
template_suffix = base_html[end_main:]

# 3. Fix the active state in prefix for user_log
template_prefix = template_prefix.replace('<li class="sub-nav-item active" onclick="location.href=\'prereg.html\'">사전예약 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'prereg.html\'">사전예약 관리</li>')

template_prefix = template_prefix.replace(
    '<li class="sub-nav-item" onclick="location.href=\'mail_all.html\'">우편 관리</li>',
    '<li class="sub-nav-item" onclick="location.href=\'mail_all.html\'">우편 관리</li>\n                        <li class="sub-nav-item active" onclick="location.href=\'user_log.html\'">유저 행동 로그</li>'
)

template_prefix = template_prefix.replace('<title>Gravity Admin Tools - 사전예약 관리</title>', '<title>Gravity Admin Tools - 유저 행동 로그</title>')

# 4. Define main content
user_log_content = """<div class="main-content">
        <div class="breadcrumb" style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px; display: flex; align-items: center; gap: 12px;">
            WEB <i class="fa-solid fa-chevron-right" style="color: #CBD5E1; font-size: 14px;"></i> GetPoring <i class="fa-solid fa-chevron-right" style="color: #CBD5E1; font-size: 14px;"></i> 유저 행동 로그
        </div>

        <div class="page-title" style="font-size: 24px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px;">
            유저 행동 로그
        </div>

        <!-- First Card: Search -->
        <div style="background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="font-size: 16px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">로그 조회</div>
            <div style="font-size: 13px; color: var(--text-gray); margin-bottom: 16px;">PlayerID 를 입력하면 해당 유저의 행동 로그를 조회합니다. (샤드는 자동 해석)</div>
            
            <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">PlayerID</div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <input type="text" style="width: 300px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px;" value="36690843045728256">
                <button style="padding: 8px 20px; font-weight: 600; background-color: var(--primary-blue); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">조회</button>
            </div>
        </div>

        <!-- Second Card: Log Table -->
        <div style="background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="display: flex; align-items: center; gap: 12px; font-size: 16px; font-weight: 700; color: var(--text-dark); margin-bottom: 20px;">
                행동 로그 — PlayerID 36690843045728256
                <span style="background-color: #F1F5F9; color: #475569; font-size: 12px; padding: 4px 8px; border-radius: 6px; font-weight: 600;">Shard 1</span>
            </div>

            <!-- Filters -->
            <div style="display: flex; gap: 16px; align-items: flex-end; margin-bottom: 24px;">
                <div>
                    <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 6px;">시작일</div>
                    <input type="date" style="padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; color: var(--text-gray);">
                </div>
                <div>
                    <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 6px;">종료일</div>
                    <input type="date" style="padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; color: var(--text-gray);">
                </div>
                <div>
                    <div style="font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 6px;">분류</div>
                    <select style="width: 150px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; color: var(--text-gray);">
                        <option>all</option>
                        <option>튜토리얼</option>
                        <option>재화</option>
                        <option>출석</option>
                    </select>
                </div>
                <div>
                    <button style="padding: 8px 20px; font-weight: 600; background-color: var(--primary-blue); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">조회</button>
                </div>
            </div>

            <!-- Table -->
            <div style="border-top: 1px solid var(--border-color);">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                    <thead style="border-bottom: 1px solid var(--border-color);">
                        <tr>
                            <th style="padding: 12px 0; font-weight: 600; color: var(--text-dark); width: 20%;">시각</th>
                            <th style="padding: 12px 0; font-weight: 600; color: var(--text-dark); width: 10%;">분류</th>
                            <th style="padding: 12px 0; font-weight: 600; color: var(--text-dark); width: 20%;">액션</th>
                            <th style="padding: 12px 0; font-weight: 600; color: var(--text-dark); width: 10%;">결과</th>
                            <th style="padding: 12px 0; font-weight: 600; color: var(--text-dark); width: 40%;">상세</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 16px 0; color: var(--text-gray);">2026. 7. 10. 오후 2:56:20</td>
                            <td style="padding: 16px 0; font-weight: 600; color: var(--text-dark);">튜토리얼</td>
                            <td style="padding: 16px 0; color: var(--text-dark);">8단계 완료</td>
                            <td style="padding: 16px 0; color: var(--text-gray);">성공</td>
                            <td style="padding: 16px 0; color: var(--text-gray);">단계 8</td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 16px 0; color: var(--text-gray);">2026. 7. 10. 오후 2:56:20</td>
                            <td style="padding: 16px 0; font-weight: 600; color: var(--text-dark);">재화</td>
                            <td style="padding: 16px 0; color: var(--text-dark);">재화 발행(faucet)</td>
                            <td style="padding: 16px 0; color: var(--text-gray);">성공</td>
                            <td style="padding: 16px 0; color: var(--text-gray);">아이템 Valhalla Pass #5 변동 <span style="color: #16A34A; font-weight: 700;">+1</span> 잔액 1 출처 튜토리얼/단계 완료</td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 16px 0; color: var(--text-gray);">2026. 7. 10. 오후 2:56:19</td>
                            <td style="padding: 16px 0; font-weight: 600; color: var(--text-dark);">출석</td>
                            <td style="padding: 16px 0; color: var(--text-dark);">출석 체크</td>
                            <td style="padding: 16px 0; color: var(--text-gray);">성공</td>
                            <td style="padding: 16px 0; color: var(--text-gray);">누적 일수 1 유형 1</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div style="text-align: center; font-size: 13px; color: #94A3B8; margin-top: 24px;">
                3건 표시
            </div>
        </div>
    </div>
"""

with open('user_log.html', 'w', encoding='utf-8') as f:
    f.write(template_prefix + user_log_content + template_suffix)


# 5. Inject new menu item into all other files that have sidebars
for file in os.listdir('.'):
    if file.endswith('.html') and file not in ['index.html', 'qna.html', 'ia.html', 'user_log.html']:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        target1 = '<li class="sub-nav-item" onclick="location.href=\'mail_all.html\'">우편 관리</li>'
        target2 = '<li class="sub-nav-item active" onclick="location.href=\'mail_all.html\'">우편 관리</li>'
        target3 = '<li class="sub-nav-item active" onclick="location.href=\'mail_individual.html\'">우편 관리</li>'
        target4 = '<li class="sub-nav-item" onclick="location.href=\'mail_individual.html\'">우편 관리</li>' # Just in case
        
        replacement = '\n                        <li class="sub-nav-item" onclick="location.href=\'user_log.html\'">유저 행동 로그</li>'
        
        if '유저 행동 로그' not in content:
            if target1 in content:
                content = content.replace(target1, target1 + replacement)
            elif target2 in content:
                content = content.replace(target2, target2 + replacement)
            elif target3 in content:
                content = content.replace(target3, target3 + replacement)
            elif target4 in content:
                content = content.replace(target4, target4 + replacement)
                
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)


# 6. Update ia.html
with open('ia.html', 'r', encoding='utf-8') as f:
    ia_content = f.read()

anchor = '<i class="fa-regular fa-file-lines text-slate-400"></i> 개별 우편 작성\n                                    </div>\n                                </li>\n                            </ul>\n                        </li>'

if anchor in ia_content and '유저 행동 로그' not in ia_content:
    new_node = """
                        <li class="relative">
                            <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                            <div class="inline-flex items-center gap-2 font-bold text-slate-700 px-2 py-1">
                                <i class="fa-regular fa-folder text-slate-400"></i> 유저 행동 로그
                            </div>
                            <ul class="pl-8 mt-2 border-l-2 border-slate-200 ml-3 space-y-2">
                                <li class="relative">
                                    <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                                    <div class="inline-flex items-center gap-2 font-semibold text-slate-600 px-2 py-1">
                                        <i class="fa-regular fa-file-lines text-slate-400"></i> 유저 행동 로그
                                    </div>
                                </li>
                            </ul>
                        </li>"""
    ia_content = ia_content.replace(anchor, anchor + new_node)
    
    with open('ia.html', 'w', encoding='utf-8') as f:
        f.write(ia_content)

print("Created user_log.html and updated all sidebars and IA.")
