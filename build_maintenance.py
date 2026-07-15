import os
import re

# 1. Base template extraction from prereg.html
with open('prereg.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

start_main = base_html.find('<div class="main-content">')
end_main = base_html.find('</body>')

template_prefix = base_html[:start_main]
template_suffix = base_html[end_main:]

# Update sidebar active state for maintenance
template_prefix = template_prefix.replace('<li class="sub-nav-item active" onclick="location.href=\'prereg.html\'">사전예약 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'prereg.html\'">사전예약 관리</li>')
template_prefix = template_prefix.replace('<li class="sub-nav-item" onclick="location.href=\'maintenance.html\'">점검 관리</li>', '<li class="sub-nav-item active" onclick="location.href=\'maintenance.html\'">점검 관리</li>')

# 2. Build maintenance.html
maintenance_content = """<div class="main-content">
        <div class="breadcrumb" style="margin-bottom: 24px; font-size: 14px; color: #64748B;">
            <i class="fa-solid fa-house" style="color: var(--admin-tools-blue); margin-right: 8px;"></i> 대시보드 <i class="fa-solid fa-chevron-right" style="margin: 0 8px; font-size: 10px;"></i> 점검 관리
        </div>

        <div class="page-title" style="font-size: 24px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px;">
            점검 관리
        </div>

        <div class="page-lnb" style="display: flex; border-bottom: 1px solid var(--border-color); margin-bottom: 24px;">
            <a href="maintenance.html" class="page-lnb-item active" style="padding: 12px 24px; font-weight: 600; color: var(--primary-blue); border-bottom: 2px solid var(--primary-blue); text-decoration: none;">점검 관리</a>
            <a href="whitelist.html" class="page-lnb-item" style="padding: 12px 24px; font-weight: 500; color: var(--text-gray); text-decoration: none;">화이트리스트</a>
        </div>

        <div class="form-card" style="background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 32px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            
            <div style="margin-bottom: 24px;">
                <div style="font-size: 16px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">현재 상태</div>
                <div style="font-size: 13px; color: var(--text-gray);">점검 on/off 및 안내 문구 (저장 시 게임 서버에 실시간 통지)</div>
            </div>

            <!-- Status Box -->
            <div id="statusBox" style="background-color: #F0FDF4; border: 1px solid #BBF7D0; color: #16A34A; padding: 16px; border-radius: 8px; font-weight: 600; font-size: 15px; margin-bottom: 20px; transition: all 0.3s;">
                현재: 정상 운영
            </div>

            <!-- Checkbox -->
            <label style="display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 24px; cursor: pointer; width: fit-content;">
                <input type="checkbox" id="maintenanceToggle" onchange="toggleMaintenance()" style="width: 16px; height: 16px; accent-color: var(--primary-blue);">
                <span id="maintenanceToggleText">점검 모드 활성화</span>
            </label>

            <!-- Textarea -->
            <div style="margin-bottom: 24px;">
                <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">안내 문구</div>
                <textarea class="form-control" style="width: 100%; height: 100px; resize: vertical; padding: 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit;" placeholder="점검 안내 문구를 입력하세요."></textarea>
            </div>

            <!-- Dates -->
            <div style="display: flex; gap: 24px; margin-bottom: 32px;">
                <div style="flex: 1;">
                    <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">시작 (UTC)</div>
                    <input type="datetime-local" class="form-control" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit;">
                </div>
                <div style="flex: 1;">
                    <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">종료 (UTC)</div>
                    <input type="datetime-local" class="form-control" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit;">
                </div>
            </div>

            <!-- Submit Button -->
            <div>
                <button id="saveBtn" class="btn btn-primary" style="padding: 10px 24px; font-weight: 600; background-color: var(--primary-blue); color: white; border: none; border-radius: 6px; cursor: pointer; transition: all 0.3s;">저장 및 통지</button>
            </div>

        </div>

        <script>
            function toggleMaintenance() {
                const toggle = document.getElementById('maintenanceToggle');
                const box = document.getElementById('statusBox');
                const btn = document.getElementById('saveBtn');
                const text = document.getElementById('maintenanceToggleText');

                if (toggle.checked) {
                    box.style.backgroundColor = '#FEF2F2';
                    box.style.borderColor = '#FECACA';
                    box.style.color = '#DC2626';
                    box.innerText = '현재: 점검 중 (로그인 차단)';
                    
                    btn.style.backgroundColor = '#EF4444';
                    btn.style.borderColor = '#EF4444';
                    
                    text.innerText = '점검 모드 해제';
                } else {
                    box.style.backgroundColor = '#F0FDF4';
                    box.style.borderColor = '#BBF7D0';
                    box.style.color = '#16A34A';
                    box.innerText = '현재: 정상 운영';
                    
                    btn.style.backgroundColor = 'var(--primary-blue)';
                    btn.style.borderColor = 'var(--primary-blue)';
                    
                    text.innerText = '점검 모드 활성화';
                }
            }
        </script>
    </div>
"""
with open('maintenance.html', 'w', encoding='utf-8') as f:
    f.write(template_prefix.replace('<title>Gravity Admin Tools - 사전예약 관리</title>', '<title>Gravity Admin Tools - 점검 관리</title>') + maintenance_content + template_suffix)

# 3. Build whitelist.html
whitelist_content = """<div class="main-content">
        <div class="breadcrumb" style="margin-bottom: 24px; font-size: 14px; color: #64748B;">
            <i class="fa-solid fa-house" style="color: var(--admin-tools-blue); margin-right: 8px;"></i> 대시보드 <i class="fa-solid fa-chevron-right" style="margin: 0 8px; font-size: 10px;"></i> 점검 관리 <i class="fa-solid fa-chevron-right" style="margin: 0 8px; font-size: 10px;"></i> 화이트리스트
        </div>

        <div class="page-title" style="font-size: 24px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px;">
            점검 관리
        </div>

        <div class="page-lnb" style="display: flex; border-bottom: 1px solid var(--border-color); margin-bottom: 24px;">
            <a href="maintenance.html" class="page-lnb-item" style="padding: 12px 24px; font-weight: 500; color: var(--text-gray); text-decoration: none;">점검 관리</a>
            <a href="whitelist.html" class="page-lnb-item active" style="padding: 12px 24px; font-weight: 600; color: var(--primary-blue); border-bottom: 2px solid var(--primary-blue); text-decoration: none;">화이트리스트</a>
        </div>

        <div class="form-card" style="background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 32px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            
            <div style="margin-bottom: 24px;">
                <div style="font-size: 16px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">화이트리스트</div>
                <div style="font-size: 13px; color: var(--text-gray);">점검 중에도 접속·플레이를 허용한 계정(AID). AID를 모르면 <a href="#" style="color: var(--primary-blue); text-decoration: none;">계정 검색</a>에서 확인 후 등록하세요.</div>
            </div>

            <!-- Input Form -->
            <div style="display: flex; gap: 16px; align-items: flex-end; margin-bottom: 32px;">
                <div style="flex: 1;">
                    <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">AID</div>
                    <input type="text" class="form-control" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit;" placeholder="예: 12345">
                </div>
                <div style="flex: 3;">
                    <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">메모 (선택)</div>
                    <input type="text" class="form-control" style="width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit;" placeholder="등록 사유">
                </div>
                <div>
                    <button class="btn btn-primary" style="padding: 10px 24px; font-weight: 600; background-color: var(--primary-blue); color: white; border: none; border-radius: 6px; cursor: pointer;">추가</button>
                </div>
            </div>

            <!-- Whitelist Table (List up) -->
            <div class="table-container" style="border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                    <thead style="background-color: var(--label-bg); border-bottom: 1px solid var(--border-color);">
                        <tr>
                            <th style="padding: 12px 16px; font-weight: 600; color: var(--text-gray); width: 20%;">AID</th>
                            <th style="padding: 12px 16px; font-weight: 600; color: var(--text-gray); width: 40%;">메모</th>
                            <th style="padding: 12px 16px; font-weight: 600; color: var(--text-gray); width: 25%;">등록일</th>
                            <th style="padding: 12px 16px; font-weight: 600; color: var(--text-gray); width: 15%; text-align: center;">관리</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 12px 16px; font-weight: 600; color: var(--text-dark);">10024</td>
                            <td style="padding: 12px 16px; color: var(--text-dark);">개발팀 테스트 계정</td>
                            <td style="padding: 12px 16px; color: var(--text-gray);">2026-07-10 14:00:00</td>
                            <td style="padding: 12px 16px; text-align: center;">
                                <button style="padding: 6px 12px; font-size: 12px; color: #EF4444; background: transparent; border: 1px solid #EF4444; border-radius: 4px; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#FEF2F2'" onmouseout="this.style.backgroundColor='transparent'">삭제</button>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 16px; font-weight: 600; color: var(--text-dark);">10055</td>
                            <td style="padding: 12px 16px; color: var(--text-dark);">QA팀 검수용 계정</td>
                            <td style="padding: 12px 16px; color: var(--text-gray);">2026-07-09 11:30:00</td>
                            <td style="padding: 12px 16px; text-align: center;">
                                <button style="padding: 6px 12px; font-size: 12px; color: #EF4444; background: transparent; border: 1px solid #EF4444; border-radius: 4px; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#FEF2F2'" onmouseout="this.style.backgroundColor='transparent'">삭제</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>
    </div>
"""
with open('whitelist.html', 'w', encoding='utf-8') as f:
    f.write(template_prefix.replace('<title>Gravity Admin Tools - 사전예약 관리</title>', '<title>Gravity Admin Tools - 화이트리스트</title>') + whitelist_content + template_suffix)

# 4. Update IA map
with open('ia.html', 'r', encoding='utf-8') as f:
    ia_content = f.read()

# Replace the 점검 관리 item in IA map with nested version
old_ia_maintenance = """<li class="relative">
                            <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                            <div class="inline-flex items-center gap-2 font-bold text-slate-700 px-2 py-1">
                                <i class="fa-regular fa-folder text-slate-400"></i> 점검 관리
                            </div>
                        </li>"""

new_ia_maintenance = """<li class="relative">
                            <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                            <div class="inline-flex items-center gap-2 font-bold text-slate-700 px-2 py-1">
                                <i class="fa-regular fa-folder text-slate-400"></i> 점검 관리
                            </div>
                            <ul class="pl-8 mt-2 border-l-2 border-slate-200 ml-3 space-y-2">
                                <li class="relative">
                                    <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                                    <div class="inline-flex items-center gap-2 font-semibold text-slate-600 px-2 py-1">
                                        <i class="fa-regular fa-file-lines text-slate-400"></i> 점검 관리 설정
                                    </div>
                                </li>
                                <li class="relative">
                                    <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                                    <div class="inline-flex items-center gap-2 font-semibold text-slate-600 px-2 py-1">
                                        <i class="fa-regular fa-file-lines text-slate-400"></i> 화이트리스트
                                    </div>
                                </li>
                            </ul>
                        </li>"""

ia_content = ia_content.replace(old_ia_maintenance, new_ia_maintenance)

with open('ia.html', 'w', encoding='utf-8') as f:
    f.write(ia_content)

print("Created maintenance and whitelist pages and updated IA map.")
