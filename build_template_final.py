import os
import re

with open('notice.html', 'r', encoding='utf-8') as f:
    notice_html = f.read()

# Extract the base HTML up to <div class="main-content">
base_parts = notice_html.split('<div class="main-content">')
base = base_parts[0] + '<div class="main-content" style="background-color: #F8FAFC; display: flex; justify-content: center; padding: 40px;">\n'

template_ui_css = """
    <style>
        .template-modal-card {
            background: #FFFFFF;
            width: 100%;
            max-width: 900px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 24px;
            border-bottom: 1px solid transparent;
        }
        
        .modal-title {
            font-size: 18px;
            font-weight: 700;
            color: #1E293B;
        }
        
        .btn-close {
            background: none;
            border: none;
            font-size: 20px;
            color: #64748B;
            cursor: pointer;
        }
        
        .modal-body {
            padding: 0 24px 24px 24px;
            flex: 1;
            overflow-y: auto;
        }
        
        /* List View Specifics */
        .list-actions {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 16px;
        }
        
        .btn-blue {
            background-color: #3B82F6;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
        }
        
        .btn-blue:hover {
            background-color: #2563EB;
        }
        
        .template-table {
            width: 100%;
            border-collapse: collapse;
            border-top: 1px solid #E2E8F0;
            border-bottom: 1px solid #E2E8F0;
        }
        
        .template-table th {
            text-align: left;
            padding: 12px 8px;
            font-size: 13px;
            color: #64748B;
            font-weight: 600;
            border-bottom: 1px solid #E2E8F0;
        }
        
        .template-table td {
            padding: 16px 8px;
            font-size: 14px;
            color: #1E293B;
            border-bottom: 1px solid #E2E8F0;
        }
        
        .template-table tr:last-child td {
            border-bottom: none;
        }
        
        .btn-sm-outline {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            color: #475569;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            margin-right: 4px;
        }
        
        /* Form View Specifics */
        .form-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 16px;
        }
        
        .input-group {
            flex: 1;
            margin-right: 24px;
        }
        
        .input-label {
            display: block;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #1E293B;
        }
        
        .template-input {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
        }
        
        .template-input:focus {
            border-color: #3B82F6;
        }
        
        .template-select {
            padding: 10px 32px 10px 12px;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
            background-color: #FFFFFF;
            min-width: 120px;
            appearance: none;
            background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%231E293B%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
            background-repeat: no-repeat;
            background-position: right 12px top 50%;
            background-size: 10px auto;
        }
        
        .help-text {
            font-size: 13px;
            color: #64748B;
            margin-bottom: 16px;
            font-weight: 500;
        }
        
        .lang-card {
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: #FFFFFF;
        }
        
        .lang-card-header {
            display: flex;
            align-items: center;
            font-size: 14px;
            font-weight: 700;
            color: #475569;
            margin-bottom: 12px;
        }
        
        .lang-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .lang-dot.red { background-color: #EF4444; }
        .lang-dot.gray { background-color: #CBD5E1; }
        
        .lang-req { color: #EF4444; margin-left: 4px; }
        
        .modal-footer {
            padding: 16px 24px;
            border-top: 1px solid #E2E8F0;
            display: flex;
            justify-content: flex-end;
            gap: 8px;
            background-color: #F8FAFC;
        }
        
        .btn-gray {
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            color: #475569;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
        }
    </style>
"""

template_html_content = template_ui_css + """
        <div class="template-modal-card">
            
            <!-- List View -->
            <div id="templateListView">
                <div class="modal-header">
                    <div class="modal-title">공지 템플릿 관리</div>
                    <button class="btn-close" onclick="location.href='notice.html'"><i class="fa-solid fa-xmark"></i></button>
                </div>
                
                <div class="modal-body">
                    <div class="list-actions">
                        <button class="btn-blue" onclick="toggleTemplateView('form')">새 템플릿</button>
                    </div>
                    
                    <table class="template-table">
                        <thead>
                            <tr>
                                <th>이름</th>
                                <th>유형</th>
                                <th>수정일</th>
                                <th>관리</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style="font-weight: 600;">test</td>
                                <td>일반</td>
                                <td style="color: #64748B;">2026. 7. 10. 오전 10:50:45</td>
                                <td>
                                    <button class="btn-sm-outline" onclick="toggleTemplateView('form')">수정</button>
                                    <button class="btn-sm-outline">삭제</button>
                                </td>
                            </tr>
                            <tr>
                                <td style="font-weight: 600;">정기 점검</td>
                                <td>점검</td>
                                <td style="color: #64748B;">2026. 7. 9. 오후 02:15:22</td>
                                <td>
                                    <button class="btn-sm-outline" onclick="toggleTemplateView('form')">수정</button>
                                    <button class="btn-sm-outline">삭제</button>
                                </td>
                            </tr>
                            <tr>
                                <td style="font-weight: 600;">여름 이벤트 당첨자</td>
                                <td>이벤트</td>
                                <td style="color: #64748B;">2026. 7. 8. 오전 11:30:00</td>
                                <td>
                                    <button class="btn-sm-outline" onclick="toggleTemplateView('form')">수정</button>
                                    <button class="btn-sm-outline">삭제</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Form View -->
            <div id="templateFormView" style="display: none; display: flex; flex-direction: column; height: 100%;">
                <div class="modal-header">
                    <div class="modal-title">공지 템플릿 관리</div>
                    <button class="btn-close" onclick="toggleTemplateView('list')"><i class="fa-solid fa-xmark"></i></button>
                </div>
                
                <div class="modal-body">
                    <div class="form-header-row">
                        <div class="input-group">
                            <label class="input-label">템플릿 이름</label>
                            <input type="text" class="template-input" value="test">
                        </div>
                        <div>
                            <select class="template-select">
                                <option value="1" selected>일반</option>
                                <option value="2">점검</option>
                                <option value="3">이벤트</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="help-text">언어별 제목·본문 — 기본 언어(한국어) 본문 필수, 작성된 언어만 게임에 노출</div>
                    
                    <div class="lang-card">
                        <div class="lang-card-header">
                            <div class="lang-dot red"></div> 한국어 <span class="lang-req">*</span>
                        </div>
                        <input type="text" class="template-input" placeholder="제목" value="테스트 공지입니다." style="margin-bottom: 8px;">
                        <textarea class="template-input" placeholder="본문" style="height: 100px; resize: vertical;">테스트 공지 내용입니다.</textarea>
                    </div>
                    
                    <div class="lang-card">
                        <div class="lang-card-header">
                            <div class="lang-dot gray"></div> English
                        </div>
                        <input type="text" class="template-input" placeholder="제목" style="margin-bottom: 8px;">
                        <textarea class="template-input" placeholder="본문" style="height: 100px; resize: vertical;"></textarea>
                    </div>
                    
                    <div class="lang-card">
                        <div class="lang-card-header">
                            <div class="lang-dot gray"></div> 日本語
                        </div>
                        <input type="text" class="template-input" placeholder="제목" style="margin-bottom: 8px;">
                        <textarea class="template-input" placeholder="본문" style="height: 100px; resize: vertical;"></textarea>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button class="btn-gray" onclick="toggleTemplateView('list')">취소</button>
                    <button class="btn-blue" onclick="alert('저장되었습니다.'); toggleTemplateView('list')">저장</button>
                </div>
            </div>
            
        </div>
    </div>
    
    <script>
        function toggleTemplateView(view) {
            if(view === 'form') {
                document.getElementById('templateListView').style.display = 'none';
                document.getElementById('templateFormView').style.display = 'flex';
            } else {
                document.getElementById('templateListView').style.display = 'block';
                document.getElementById('templateFormView').style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

# Re-inject styles and script into base
# notice_html has styles inside <head>. We need to add template_ui_css inside <head> as well.
head_split = base.split('</head>')
final_html = head_split[0] + template_ui_css + '</head>' + head_split[1] + template_html_content.replace(template_ui_css, '')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("template.html rebuilt perfectly mimicking the screenshot.")
