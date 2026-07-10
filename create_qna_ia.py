import os

# --- 1. Update index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Replace the QnA accordion with a simple link to qna.html
qna_link_html = """<!-- Item 3: 주요 질의사항 -->
                <a href="qna.html" class="group relative flex items-center justify-between p-3.5 px-5 bg-white/60 hover:bg-white border border-white/80 hover:border-rose-200 rounded-2xl transition-all duration-500 shadow-sm hover:shadow-xl hover:-translate-y-1 overflow-hidden w-full text-left">
                    <div class="absolute inset-0 bg-gradient-to-r from-rose-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                    <div class="flex items-center gap-5 z-10">
                        <div class="w-12 h-12 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-500 shadow-inner">❓</div>
                        <div>
                            <div class="text-[13px] font-bold text-rose-500 mb-0.5 tracking-wide">Q & A</div>
                            <div class="text-[19px] font-extrabold text-slate-800">주요 질의사항</div>
                        </div>
                    </div>
                    <div class="w-10 h-10 rounded-full bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-400 group-hover:bg-rose-500 group-hover:text-white group-hover:border-rose-500 transition-all duration-500 z-10">
                        <svg class="w-5 h-5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"></path></svg>
                    </div>
                </a>
"""

start_idx = index_html.find('<!-- Item 3: 주요 질의사항 -->')
end_idx = index_html.find('            </div>\n        </div>\n    </div>\n</body>')

if start_idx != -1 and end_idx != -1:
    index_html = index_html[:start_idx] + qna_link_html + index_html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)


# --- 2. Create qna.html and ia.html ---
# We will use prereg.html as a base template for the Admin UI layout.
with open('prereg.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

start_main = base_html.find('<div class="main-content">')
end_main = base_html.find('</body>')

template_prefix = base_html[:start_main]
template_suffix = base_html[end_main:]

# Remove active state from sidebar
template_prefix = template_prefix.replace('<li class="sub-nav-item active" onclick="location.href=\'prereg.html\'">사전예약 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'prereg.html\'">사전예약 관리</li>')

# --- qna.html ---
qna_content = """<div class="main-content" style="background-color: #F8FAFC; padding: 40px;">
        <div class="breadcrumb" style="margin-bottom: 24px; font-size: 14px; color: #64748B;">
            <i class="fa-solid fa-house" style="color: var(--admin-tools-blue); margin-right: 8px;"></i> 대시보드 <i class="fa-solid fa-chevron-right" style="margin: 0 8px; font-size: 10px;"></i> 주요 질의사항
        </div>
        
        <div style="font-size: 24px; font-weight: 700; color: var(--text-dark); margin-bottom: 32px; display: flex; align-items: center; gap: 12px;">
            <div style="width: 48px; height: 48px; border-radius: 12px; background: #FFE4E6; color: #E11D48; display: flex; align-items: center; justify-content: center; font-size: 24px;">❓</div>
            주요 질의사항 (Q&A)
        </div>

        <div style="background: white; border: 1px solid var(--border-color); border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
            <div style="font-size: 16px; font-weight: 600; color: var(--text-dark); margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border-color);">
                API 수급 필요 리스트
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 16px;">
                <div style="background: #F8FAFC; border-radius: 8px; padding: 20px; border-left: 4px solid var(--admin-tools-blue); display: flex; align-items: center; gap: 16px;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: #E2E8F0; color: #475569; display: flex; align-items: center; justify-content: center; font-weight: 700;">1</div>
                    <div style="font-weight: 600; color: var(--text-dark); font-size: 16px;">우편 관리 > 등록 템플릿 > 조회 API 수급 필요</div>
                </div>
                
                <div style="background: #F8FAFC; border-radius: 8px; padding: 20px; border-left: 4px solid var(--admin-tools-blue); display: flex; align-items: center; gap: 16px;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: #E2E8F0; color: #475569; display: flex; align-items: center; justify-content: center; font-weight: 700;">2</div>
                    <div style="font-weight: 600; color: var(--text-dark); font-size: 16px;">단건 우편 발송의 건 이력 조회 API 수급 필요</div>
                </div>
            </div>
            
            <div style="margin-top: 40px; display: flex; justify-content: flex-end;">
                <button class="btn btn-outline" style="padding: 10px 24px; display: flex; align-items: center; gap: 8px;" onclick="location.href='index.html'">
                    <i class="fa-solid fa-arrow-left"></i> 대시보드로 돌아가기
                </button>
            </div>
        </div>
    </div>
"""
with open('qna.html', 'w', encoding='utf-8') as f:
    f.write(template_prefix.replace('<title>Gravity Admin Tools - 사전예약 관리</title>', '<title>Gravity Admin Tools - 주요 질의사항</title>') + qna_content + template_suffix)


# --- ia.html ---
ia_content = """<div class="main-content" style="background-color: #F8FAFC; padding: 40px;">
        <div class="breadcrumb" style="margin-bottom: 24px; font-size: 14px; color: #64748B;">
            <i class="fa-solid fa-house" style="color: var(--admin-tools-blue); margin-right: 8px;"></i> 대시보드 <i class="fa-solid fa-chevron-right" style="margin: 0 8px; font-size: 10px;"></i> IA (정보구조도) 맵
        </div>
        
        <div style="font-size: 24px; font-weight: 700; color: var(--text-dark); margin-bottom: 32px; display: flex; align-items: center; gap: 12px;">
            <div style="width: 48px; height: 48px; border-radius: 12px; background: #CFFAFE; color: #0891B2; display: flex; align-items: center; justify-content: center; font-size: 24px;">🗺️</div>
            IA (정보구조도) 맵 - Get Poring
        </div>

        <div style="background: white; border: 1px solid var(--border-color); border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
            <div style="font-size: 16px; font-weight: 600; color: var(--text-dark); margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border-color);">
                Get Poring GM Tool Menu Structure
            </div>
            
            <ul style="list-style: none; padding-left: 0; font-size: 16px; font-family: 'Pretendard Variable', sans-serif;">
                <li style="margin-bottom: 20px;">
                    <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 800; color: #1e293b; background: #F1F5F9; padding: 8px 16px; border-radius: 8px; border: 1px solid #E2E8F0;">
                        <i class="fa-solid fa-gamepad" style="color: var(--admin-tools-blue);"></i> Get Poring
                    </div>
                    
                    <ul style="list-style: none; padding-left: 32px; margin-top: 16px; border-left: 2px solid #E2E8F0; margin-left: 16px;">
                        
                        <li style="position: relative; margin-bottom: 16px;">
                            <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                            <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: #334155; padding: 4px 8px;">
                                <i class="fa-regular fa-folder" style="color: #64748B;"></i> 사전예약 관리 <span style="font-size: 12px; font-weight: 400; color: #94A3B8; margin-left: 8px;">(prereg.html)</span>
                            </div>
                        </li>
                        
                        <li style="position: relative; margin-bottom: 16px;">
                            <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                            <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: #334155; padding: 4px 8px;">
                                <i class="fa-regular fa-folder" style="color: #64748B;"></i> 공지 관리 <span style="font-size: 12px; font-weight: 400; color: #94A3B8; margin-left: 8px;">(notice.html)</span>
                            </div>
                            <ul style="list-style: none; padding-left: 32px; margin-top: 8px; border-left: 2px solid #E2E8F0; margin-left: 12px;">
                                <li style="position: relative; margin-bottom: 8px;">
                                    <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                                    <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 500; color: #475569; padding: 4px 8px;">
                                        <i class="fa-regular fa-file-lines" style="color: #94A3B8;"></i> 공지 등록/수정 <span style="font-size: 12px; font-weight: 400; color: #CBD5E1; margin-left: 8px;">(notice_form.html)</span>
                                    </div>
                                </li>
                            </ul>
                        </li>
                        
                        <li style="position: relative; margin-bottom: 16px;">
                            <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                            <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: #334155; padding: 4px 8px;">
                                <i class="fa-regular fa-folder" style="color: #64748B;"></i> 점검 관리 <span style="font-size: 12px; font-weight: 400; color: #94A3B8; margin-left: 8px;">(maintenance.html)</span>
                            </div>
                        </li>
                        
                        <li style="position: relative; margin-bottom: 16px;">
                            <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                            <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: #334155; padding: 4px 8px;">
                                <i class="fa-regular fa-folder" style="color: #64748B;"></i> 우편 관리
                            </div>
                            <ul style="list-style: none; padding-left: 32px; margin-top: 8px; border-left: 2px solid #E2E8F0; margin-left: 12px;">
                                <li style="position: relative; margin-bottom: 8px;">
                                    <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                                    <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 500; color: #475569; padding: 4px 8px;">
                                        <i class="fa-regular fa-file-lines" style="color: #94A3B8;"></i> 전체 우편 리스트 <span style="font-size: 12px; font-weight: 400; color: #CBD5E1; margin-left: 8px;">(mail_all.html)</span>
                                    </div>
                                </li>
                                <li style="position: relative; margin-bottom: 8px;">
                                    <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                                    <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 500; color: #475569; padding: 4px 8px;">
                                        <i class="fa-regular fa-file-lines" style="color: #94A3B8;"></i> 전체 우편 작성 <span style="font-size: 12px; font-weight: 400; color: #CBD5E1; margin-left: 8px;">(mail_all_form.html)</span>
                                    </div>
                                </li>
                                <li style="position: relative; margin-bottom: 8px;">
                                    <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                                    <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 500; color: #475569; padding: 4px 8px;">
                                        <i class="fa-regular fa-file-lines" style="color: #94A3B8;"></i> 개별 우편 리스트 <span style="font-size: 12px; font-weight: 400; color: #CBD5E1; margin-left: 8px;">(mail_individual.html)</span>
                                    </div>
                                </li>
                                <li style="position: relative; margin-bottom: 8px;">
                                    <span style="position: absolute; left: -32px; top: 12px; width: 24px; height: 2px; background-color: #E2E8F0;"></span>
                                    <div style="display: inline-flex; align-items: center; gap: 8px; font-weight: 500; color: #475569; padding: 4px 8px;">
                                        <i class="fa-regular fa-file-lines" style="color: #94A3B8;"></i> 개별 우편 작성 <span style="font-size: 12px; font-weight: 400; color: #CBD5E1; margin-left: 8px;">(mail_individual_form.html)</span>
                                    </div>
                                </li>
                            </ul>
                        </li>
                        
                    </ul>
                </li>
            </ul>
            
            <div style="margin-top: 40px; display: flex; justify-content: flex-end;">
                <button class="btn btn-outline" style="padding: 10px 24px; display: flex; align-items: center; gap: 8px;" onclick="location.href='index.html'">
                    <i class="fa-solid fa-arrow-left"></i> 대시보드로 돌아가기
                </button>
            </div>
        </div>
    </div>
"""
with open('ia.html', 'w', encoding='utf-8') as f:
    f.write(template_prefix.replace('<title>Gravity Admin Tools - 사전예약 관리</title>', '<title>Gravity Admin Tools - IA 맵</title>') + ia_content + template_suffix)

print("Created qna.html and ia.html. Updated index.html.")
