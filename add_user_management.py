import os
import re

# 1. Base template extraction
with open('prereg.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

start_main = base_html.find('<div class="main-content">')
end_main = base_html.find('</body>')

template_prefix = base_html[:start_main]
template_suffix = base_html[end_main:]

# Update sidebar active state
template_prefix = template_prefix.replace('<li class="sub-nav-item active" onclick="location.href=\'prereg.html\'">사전예약 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'prereg.html\'">사전예약 관리</li>')

# Add the new LNB item to the prefix for the new file
# Find where '유저 행동 로그' is added and insert before it
# Wait, prereg.html has '유저 행동 로그' now because we updated it.
target_log = '<li class="sub-nav-item" onclick="location.href=\'user_log.html\'">유저 행동 로그</li>'
new_item_active = '<li class="sub-nav-item active" onclick="location.href=\'user_management.html\'">게임 유저 관리</li>\n                        '
if target_log in template_prefix:
    template_prefix = template_prefix.replace(target_log, new_item_active + target_log)

# Change Title
template_prefix = template_prefix.replace('<title>Gravity Admin Tools - 사전예약 관리</title>', '<title>Gravity Admin Tools - 게임 유저 관리</title>')

# 2. Main Content
main_content = """<div class="main-content">
        <div class="breadcrumb" style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px; display: flex; align-items: center; gap: 12px;">
            WEB <i class="fa-solid fa-chevron-right" style="color: #CBD5E1; font-size: 14px;"></i> GetPoring <i class="fa-solid fa-chevron-right" style="color: #CBD5E1; font-size: 14px;"></i> 게임 유저 관리
        </div>

        <div class="page-title" style="font-size: 24px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px;">
            게임 유저 관리
        </div>

        <!-- First Card: Search -->
        <div style="background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="font-size: 16px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px;">유저 검색</div>
            <div style="font-size: 13px; color: var(--text-gray); margin-bottom: 16px;">AID-PlayerID(숫자) 또는 채널(외부신원)로 검색합니다.</div>
            
            <div style="display: flex; gap: 12px; align-items: flex-end;">
                <div>
                    <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">검색 유형</div>
                    <select style="width: 150px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; color: var(--text-dark);">
                        <option>playerId</option>
                        <option>AID</option>
                        <option>채널(외부신원)</option>
                    </select>
                </div>
                <div>
                    <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">검색어</div>
                    <input type="text" style="width: 300px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px;" value="36690843045728256">
                </div>
                <div>
                    <button style="padding: 8px 24px; font-weight: 600; background-color: var(--primary-blue); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">검색</button>
                </div>
            </div>
        </div>

        <!-- Second Card: Result -->
        <div style="background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="font-size: 16px; font-weight: 700; color: var(--text-dark); margin-bottom: 24px;">검색 결과</div>
            
            <!-- User Info Summary -->
            <div style="display: flex; gap: 80px; margin-bottom: 24px; font-size: 14px;">
                <div>
                    <div style="margin-bottom: 12px;"><span style="color: var(--text-gray); width: 60px; display: inline-block;">AID</span> <span style="color: var(--primary-blue); font-weight: 600;">36690841913266176</span></div>
                    <div><span style="color: var(--text-gray); width: 60px; display: inline-block;">계정상태</span> <span style="color: #EF4444; font-weight: 600;">정지(SUSPEND)</span></div>
                </div>
                <div>
                    <div style="margin-bottom: 12px;"><span style="color: var(--text-gray); width: 80px; display: inline-block;">연동</span> <span style="font-weight: 600; color: var(--text-dark);">게스트</span></div>
                    <div><span style="color: var(--text-gray); width: 80px; display: inline-block;">마지막 로그인</span> <span style="color: var(--text-dark);">2026. 7. 10. 오후 2:56:18</span></div>
                </div>
                <div>
                    <div style="margin-bottom: 12px;"><span style="color: var(--text-gray); width: 60px; display: inline-block;">플랫폼</span> <span style="color: var(--text-dark);">Guest</span></div>
                </div>
            </div>

            <!-- Channel Link Table -->
            <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">연동 채널</div>
            <div style="border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; margin-bottom: 24px;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                    <thead style="background-color: var(--label-bg); border-bottom: 1px solid var(--border-color);">
                        <tr>
                            <th style="padding: 12px 16px; width: 15%; font-weight: 600; color: var(--text-gray);">채널</th>
                            <th style="padding: 12px 16px; width: 60%; font-weight: 600; color: var(--text-gray);">외부 식별자(ThirdPartyID)</th>
                            <th style="padding: 12px 16px; width: 25%; font-weight: 600; color: var(--text-gray);">연동일</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 16px;">
                                <span style="background-color: #F1F5F9; color: #475569; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 8px;">게스트</span> <span style="color: #94A3B8; font-size: 13px;">기반 계정</span>
                            </td>
                            <td style="padding: 16px; color: var(--primary-blue);">DijeM2hg6KDLm7zsdJ3g0bt_2Wqrp0h2UAHBRUC9Gmg</td>
                            <td style="padding: 16px; color: var(--text-dark);">2026. 7. 10. 오후 2:56:18</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Sanction Info Box -->
            <div style="background-color: #F8FAFC; border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 14px;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                        <span style="color: var(--text-gray); font-weight: 600; width: 60px;">계정 제재:</span>
                        <span style="color: #EF4444; font-weight: 700;">제재 중 — test (만료 2026. 7. 11. 오후 3:14:00)</span>
                        <button style="background: white; border: 1px solid var(--border-color); padding: 4px 10px; border-radius: 4px; font-size: 12px; color: var(--text-dark); cursor: pointer;">계정 해제</button>
                    </div>
                    <div>
                        <span style="color: var(--text-gray); font-weight: 600; width: 60px; display: inline-block;">채팅 제재:</span>
                        <span style="color: var(--text-dark);">없음</span>
                    </div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button style="background: white; border: 1px solid var(--border-color); padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; color: var(--text-dark); cursor: pointer;">강제 로그아웃</button>
                    <button style="background-color: #FEE2E2; color: #EF4444; border: none; padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;" onclick="openModal('sanctionModal')">제재</button>
                    <button style="background-color: #FEE2E2; color: #EF4444; border: none; padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;" onclick="openModal('deleteModal')">계정 삭제</button>
                </div>
            </div>

            <!-- Timeline Accordion -->
            <div style="border: 1px solid var(--border-color); border-radius: 8px; margin-bottom: 24px; overflow: hidden;">
                <div style="padding: 16px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; background-color: var(--white);">
                    <div>
                        <span style="font-weight: 600; color: var(--text-dark); font-size: 14px;">활동 타임라인</span> <span style="color: #94A3B8; font-size: 13px; margin-left: 8px;">(제재·변경이력)</span>
                    </div>
                    <div style="color: #94A3B8; font-size: 13px;">
                        펼치기 <i class="fa-solid fa-chevron-down ml-1"></i>
                    </div>
                </div>
            </div>

            <!-- Player List Table -->
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                <thead style="border-bottom: 1px solid var(--border-color);">
                    <tr>
                        <th style="padding: 16px 8px; width: 40%; font-weight: 600; color: var(--text-gray);">PlayerID</th>
                        <th style="padding: 16px 8px; width: 20%; font-weight: 600; color: var(--text-gray);">ShardID</th>
                        <th style="padding: 16px 8px; width: 30%; font-weight: 600; color: var(--text-gray);">생성일</th>
                        <th style="padding: 16px 8px; width: 10%; font-weight: 600; color: var(--text-gray);">상세</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 16px 8px; color: var(--primary-blue); font-weight: 600;">36690843045728256</td>
                        <td style="padding: 16px 8px; color: var(--text-dark);">1</td>
                        <td style="padding: 16px 8px; color: var(--text-dark);">2026. 7. 10.</td>
                        <td style="padding: 16px 8px;">
                            <button style="background: white; border: 1px solid var(--border-color); padding: 4px 12px; border-radius: 4px; font-size: 12px; color: var(--text-dark); cursor: pointer;">상세</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Sanction Modal -->
        <div id="sanctionModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1000; align-items: center; justify-content: center;">
            <div style="background: white; width: 420px; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
                <div style="padding: 20px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 18px; font-weight: 700; color: var(--text-dark);">계정 제재 — AID 36690841913266176</div>
                    <i class="fa-solid fa-xmark" style="cursor: pointer; font-size: 18px; color: #94A3B8;" onclick="closeModal('sanctionModal')"></i>
                </div>
                <div style="padding: 24px;">
                    <div style="font-size: 13px; color: #64748B; margin-bottom: 24px; line-height: 1.5;">
                        사유는 필수입니다. 만료일을 비우면 영구 제재입니다. (로그인은 NORMAL 만 허용)
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">제재 유형</div>
                        <select style="width: 100%; padding: 10px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; color: var(--text-dark);">
                            <option>영구정지(BAN)</option>
                            <option selected>정지(SUSPEND)</option>
                            <option>채팅금지</option>
                        </select>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">사유 (필수)</div>
                        <input type="text" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px;">
                    </div>
                    
                    <div style="margin-bottom: 12px;">
                        <div style="font-size: 14px; font-weight: 600; color: var(--text-dark); margin-bottom: 8px;">만료일 (선택, 비우면 영구)</div>
                        <input type="datetime-local" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; color: var(--text-gray);">
                    </div>
                </div>
                <div style="padding: 16px 24px; background: #F8FAFC; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; gap: 12px;">
                    <button style="background: white; border: 1px solid var(--border-color); padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 600; color: var(--text-dark); cursor: pointer;" onclick="closeModal('sanctionModal')">취소</button>
                    <button style="background-color: #FEE2E2; color: #EF4444; border: none; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer;">제재 적용</button>
                </div>
            </div>
        </div>

        <!-- Delete Modal -->
        <div id="deleteModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1000; align-items: center; justify-content: center;">
            <div style="background: white; width: 450px; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
                <div style="padding: 20px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 18px; font-weight: 700; color: var(--text-dark);">계정 삭제</div>
                    <i class="fa-solid fa-xmark" style="cursor: pointer; font-size: 18px; color: #94A3B8;" onclick="closeModal('deleteModal')"></i>
                </div>
                <div style="padding: 24px;">
                    <div style="font-size: 13px; color: #64748B; margin-bottom: 24px; line-height: 1.5;">
                        계정을 삭제(소프트)하고 모든 채널 연동을 해제합니다. 잔존 캐시(세션·플레이어)도 함께 정리됩니다. 게임 데이터(플레이어)는 보존됩니다.
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <div style="font-size: 14px; color: var(--text-gray); margin-bottom: 8px;">확인을 위해 <span style="color: var(--text-dark); font-weight: 700;">36690841913266176</span> 을(를) 입력하세요</div>
                        <input type="text" style="width: 100%; padding: 10px 12px; border: 1px solid var(--primary-blue); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; box-shadow: 0 0 0 3px rgba(82, 130, 255, 0.15);">
                    </div>
                    
                    <div style="margin-bottom: 12px;">
                        <div style="font-size: 14px; font-weight: 600; color: var(--text-gray); margin-bottom: 8px;">사유 (필수)</div>
                        <textarea style="width: 100%; height: 80px; resize: none; padding: 10px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-family: inherit; font-size: 14px;"></textarea>
                    </div>
                </div>
                <div style="padding: 16px 24px; background: #F8FAFC; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; gap: 12px;">
                    <button style="background: white; border: 1px solid var(--border-color); padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 600; color: var(--text-dark); cursor: pointer;" onclick="closeModal('deleteModal')">취소</button>
                    <button style="background-color: #FEE2E2; color: #EF4444; border: none; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer;">삭제</button>
                </div>
            </div>
        </div>

        <script>
        function openModal(id) {
            document.getElementById(id).style.display = 'flex';
        }
        function closeModal(id) {
            document.getElementById(id).style.display = 'none';
        }
        </script>
    </div>
"""

with open('user_management.html', 'w', encoding='utf-8') as f:
    f.write(template_prefix + main_content + template_suffix)


# 3. Add to sidebar in all files
target_log_normal = '<li class="sub-nav-item" onclick="location.href=\'user_log.html\'">유저 행동 로그</li>'
target_log_active = '<li class="sub-nav-item active" onclick="location.href=\'user_log.html\'">유저 행동 로그</li>'
new_item_normal = '<li class="sub-nav-item" onclick="location.href=\'user_management.html\'">게임 유저 관리</li>\n                        '

for file in os.listdir('.'):
    if file.endswith('.html') and file not in ['index.html', 'qna.html', 'ia.html', 'user_management.html']:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '게임 유저 관리' not in content:
            if target_log_normal in content:
                content = content.replace(target_log_normal, new_item_normal + target_log_normal)
            elif target_log_active in content:
                content = content.replace(target_log_active, new_item_normal + target_log_active)
                
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)


# 4. Update ia.html
with open('ia.html', 'r', encoding='utf-8') as f:
    ia_content = f.read()

# Find the anchor for 유저 행동 로그
# We inserted it previously as:
# <i class="fa-regular fa-folder text-slate-400"></i> 유저 행동 로그
# Let's insert '게임 유저 관리' right before '유저 행동 로그'
anchor = """<li class="relative">
                            <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                            <div class="inline-flex items-center gap-2 font-bold text-slate-700 px-2 py-1">
                                <i class="fa-regular fa-folder text-slate-400"></i> 유저 행동 로그"""

new_node = """<li class="relative">
                            <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                            <div class="inline-flex items-center gap-2 font-bold text-slate-700 px-2 py-1">
                                <i class="fa-regular fa-folder text-slate-400"></i> 게임 유저 관리
                            </div>
                            <ul class="pl-8 mt-2 border-l-2 border-slate-200 ml-3 space-y-2">
                                <li class="relative">
                                    <span class="absolute -left-8 top-3 w-6 h-0.5 bg-slate-200"></span>
                                    <div class="inline-flex items-center gap-2 font-semibold text-slate-600 px-2 py-1">
                                        <i class="fa-regular fa-file-lines text-slate-400"></i> 게임 유저 관리
                                    </div>
                                </li>
                            </ul>
                        </li>
                        """

if anchor in ia_content and '게임 유저 관리' not in ia_content:
    ia_content = ia_content.replace(anchor, new_node + anchor)
    with open('ia.html', 'w', encoding='utf-8') as f:
        f.write(ia_content)

print("Created user_management.html and updated all sidebars and IA.")
