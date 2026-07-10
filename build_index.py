import os

with open('prereg.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Replace main-content with Dashboard content
start_idx = base_html.find('<div class="main-content">')

dashboard_html = """<div class="main-content" style="background-color: #F8FAFC;">
        <div class="breadcrumb" style="margin-bottom: 32px;">
            <i class="fa-solid fa-house" style="color: var(--admin-tools-blue); margin-right: 8px;"></i> 대시보드
        </div>

        <div class="dashboard-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
            
            <!-- 어드민 기획서 -->
            <div class="dash-card" style="background: var(--white); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                <div class="dash-title" style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 20px; display: flex; align-items: center; gap: 8px;">
                    <i class="fa-solid fa-file-lines" style="color: var(--admin-tools-blue);"></i> 어드민 기획서
                </div>
                <div style="font-size: 14px; color: var(--text-gray); line-height: 1.6;">
                    <p style="margin-bottom: 12px;">현재 작업 중인 기획서 및 산출물 문서를 확인할 수 있습니다.</p>
                    <a href="#" class="btn btn-outline" style="display: inline-flex; align-items: center; gap: 8px; text-decoration: none;">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i> 기획서 보기 (Notion/Google Docs)
                    </a>
                </div>
            </div>

            <!-- 사이트맵 -->
            <div class="dash-card" style="background: var(--white); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                <div class="dash-title" style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 20px; display: flex; align-items: center; gap: 8px;">
                    <i class="fa-solid fa-sitemap" style="color: var(--admin-tools-blue);"></i> 사이트맵 (GetPoring)
                </div>
                <ul style="list-style: none; padding-left: 0; font-size: 15px;">
                    <li style="margin-bottom: 12px;">
                        <a href="prereg.html" style="color: var(--text-dark); text-decoration: none; font-weight: 600; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-dark)'">사전예약 관리</a>
                    </li>
                    <li style="margin-bottom: 12px;">
                        <a href="notice.html" style="color: var(--text-dark); text-decoration: none; font-weight: 600; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-dark)'">공지 관리</a>
                        <ul style="list-style: none; padding-left: 24px; margin-top: 8px; border-left: 2px solid #E2E8F0; margin-left: 8px;">
                            <li style="position: relative; margin-bottom: 8px;">
                                <span style="position: absolute; left: -24px; top: 10px; width: 16px; height: 2px; background-color: #E2E8F0;"></span>
                                <a href="notice_form.html" style="color: var(--text-gray); text-decoration: none; font-weight: 500; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-gray)'">공지 등록/수정</a>
                            </li>
                        </ul>
                    </li>
                    <li style="margin-bottom: 12px;">
                        <a href="maintenance.html" style="color: var(--text-dark); text-decoration: none; font-weight: 600; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-dark)'">점검 관리</a>
                    </li>
                    <li style="margin-bottom: 12px;">
                        <a href="mail_all.html" style="color: var(--text-dark); text-decoration: none; font-weight: 600; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-dark)'">우편 관리</a>
                        <ul style="list-style: none; padding-left: 24px; margin-top: 8px; border-left: 2px solid #E2E8F0; margin-left: 8px;">
                            <li style="position: relative; margin-bottom: 8px;">
                                <span style="position: absolute; left: -24px; top: 10px; width: 16px; height: 2px; background-color: #E2E8F0;"></span>
                                <a href="mail_all.html" style="color: var(--text-gray); text-decoration: none; font-weight: 500; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-gray)'">전체 우편 리스트</a>
                            </li>
                            <li style="position: relative; margin-bottom: 8px;">
                                <span style="position: absolute; left: -24px; top: 10px; width: 16px; height: 2px; background-color: #E2E8F0;"></span>
                                <a href="mail_all_form.html" style="color: var(--text-gray); text-decoration: none; font-weight: 500; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-gray)'">전체 우편 작성</a>
                            </li>
                            <li style="position: relative; margin-bottom: 8px;">
                                <span style="position: absolute; left: -24px; top: 10px; width: 16px; height: 2px; background-color: #E2E8F0;"></span>
                                <a href="mail_individual.html" style="color: var(--text-gray); text-decoration: none; font-weight: 500; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-gray)'">개별 우편 리스트</a>
                            </li>
                            <li style="position: relative; margin-bottom: 8px;">
                                <span style="position: absolute; left: -24px; top: 10px; width: 16px; height: 2px; background-color: #E2E8F0;"></span>
                                <a href="mail_individual_form.html" style="color: var(--text-gray); text-decoration: none; font-weight: 500; display: inline-block; padding: 4px 8px; border-radius: 4px; transition: background 0.2s;" onmouseover="this.style.backgroundColor='#F1F5F9'; this.style.color='#3b82f6'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='var(--text-gray)'">개별 우편 작성</a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>

            <!-- 질의 사항 -->
            <div class="dash-card" style="grid-column: 1 / -1; background: var(--white); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                <div class="dash-title" style="font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 20px; display: flex; align-items: center; gap: 8px;">
                    <i class="fa-solid fa-circle-question" style="color: var(--admin-tools-blue);"></i> 주요 질의 사항 (Q&A / 기획 확인 필요)
                </div>
                
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 16px; border-left: 4px solid var(--admin-tools-blue);">
                        <div style="font-weight: 700; color: var(--text-dark); margin-bottom: 8px; font-size: 15px;"><i class="fa-solid fa-q" style="color: var(--admin-tools-blue); margin-right: 6px;"></i> 사전예약 보상 지급 로직</div>
                        <div style="color: var(--text-gray); font-size: 14px; line-height: 1.5; padding-left: 24px;">사전예약 보상 발송 시, 어드민의 우편 시스템 API를 통해 글로벌하게 자동 일괄 발송되는 구조인지, 아니면 별도의 쿠폰 코드로 발급되는 방식인지 명확한 확인이 필요합니다.</div>
                    </div>
                    
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 16px; border-left: 4px solid var(--admin-tools-blue);">
                        <div style="font-weight: 700; color: var(--text-dark); margin-bottom: 8px; font-size: 15px;"><i class="fa-solid fa-q" style="color: var(--admin-tools-blue); margin-right: 6px;"></i> 다국어(현지화) 데이터 관리 범위</div>
                        <div style="color: var(--text-gray); font-size: 14px; line-height: 1.5; padding-left: 24px;">공지와 우편 템플릿의 텍스트가 인게임에서 Key 값으로 매핑되어 자동 현지화된다고 하셨는데, 어드민 툴 내부에서도 각 언어별 실제 번역된 텍스트 값을 조회하거나 미리보기(Preview) 할 수 있는 부가 기능이 필요한가요?</div>
                    </div>
                    
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 16px; border-left: 4px solid var(--admin-tools-blue);">
                        <div style="font-weight: 700; color: var(--text-dark); margin-bottom: 8px; font-size: 15px;"><i class="fa-solid fa-q" style="color: var(--admin-tools-blue); margin-right: 6px;"></i> 어드민 권한 관리 (Role & Permission)</div>
                        <div style="color: var(--text-gray); font-size: 14px; line-height: 1.5; padding-left: 24px;">현재 어드민 툴의 메뉴별 접근 및 액션 권한(읽기/쓰기/발송 승인 등)을 계정 등급(예: 일반 GM, 팀장급)별로 세분화하여 제어해야 하는지 기획적인 확정이 필요합니다.</div>
                    </div>

                    <div style="background: #F8FAFC; border-radius: 8px; padding: 16px; border-left: 4px solid var(--admin-tools-blue);">
                        <div style="font-weight: 700; color: var(--text-dark); margin-bottom: 8px; font-size: 15px;"><i class="fa-solid fa-q" style="color: var(--admin-tools-blue); margin-right: 6px;"></i> 샤드(Shard) 일괄 적용 예외 처리</div>
                        <div style="color: var(--text-gray); font-size: 14px; line-height: 1.5; padding-left: 24px;">공지나 우편을 여러 샤드에 동시 적용할 때, 일부 샤드에서 API 타임아웃이나 네트워크 에러가 발생할 경우, 자동 부분 롤백(Rollback)을 지원해야 하는지 혹은 개별 샤드별 재시도(Retry) 버튼을 UI로 제공해야 하는지 확인 부탁드립니다.</div>
                    </div>
                    
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 16px; border-left: 4px solid var(--admin-tools-blue);">
                        <div style="font-weight: 700; color: var(--text-dark); margin-bottom: 8px; font-size: 15px;"><i class="fa-solid fa-q" style="color: var(--admin-tools-blue); margin-right: 6px;"></i> 어드민 활동 로그 (Audit Log) 관리</div>
                        <div style="color: var(--text-gray); font-size: 14px; line-height: 1.5; padding-left: 24px;">보안상 GM의 모든 주요 작업(전체 우편 발송, 보상 지급, 공지 등록 등)에 대한 활동 이력을 추적하고 조회할 수 있는 별도의 '운영 로그' 페이지가 포함되어야 하는지 검토 바랍니다.</div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</body>
</html>"""

new_content = base_html[:start_idx] + dashboard_html

# Un-highlight the sidebar item and update title
new_content = new_content.replace('<li class="sub-nav-item active" onclick="location.href=\'prereg.html\'">사전예약 관리</li>', '<li class="sub-nav-item" onclick="location.href=\'prereg.html\'">사전예약 관리</li>')
new_content = new_content.replace('<title>Gravity Admin Tools - 사전예약 관리</title>', '<title>Gravity Admin Tools - 대시보드</title>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Created index.html dashboard.")
