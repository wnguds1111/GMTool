import os
import re

with open('user_management.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS classes to <style>
new_css = """
        .form-card {
            background-color: var(--white);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 14px;
        }
        .data-table th, .data-table td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
        }
        .data-table th {
            background-color: var(--label-bg);
            font-weight: 600;
            color: var(--text-gray);
        }
        .page-lnb {
            display: flex;
            gap: 24px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
            padding: 0 16px;
        }
        .page-lnb-item {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-gray);
            padding-bottom: 12px;
            cursor: pointer;
            position: relative;
        }
        .page-lnb-item.active {
            color: var(--primary-blue);
        }
        .page-lnb-item.active::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 3px;
            background-color: var(--primary-blue);
            border-radius: 3px 3px 0 0;
        }
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(2px);
        }
        .modal-content-large {
            background: white;
            width: 1000px;
            max-height: 90vh;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            overflow: hidden;
        }
        .modal-header {
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
        }
        .modal-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-dark);
        }
        .modal-body {
            padding: 0;
            overflow-y: auto;
            flex: 1;
        }
        .tab-content {
            display: none;
            padding: 24px;
            background: #F8FAFC;
        }
        .tab-content.active {
            display: block;
        }
"""
if '.modal-content-large' not in content:
    content = content.replace('</style>', new_css + '    </style>')

# 2. Bind the button
target_btn = '<button style="background: white; border: 1px solid var(--border-color); padding: 4px 12px; border-radius: 4px; font-size: 12px; color: var(--text-dark); cursor: pointer;">상세</button>'
replacement_btn = '<button style="background: white; border: 1px solid var(--border-color); padding: 4px 12px; border-radius: 4px; font-size: 12px; color: var(--text-dark); cursor: pointer;" onclick="openModal(\'playerDetailsModal\')">상세</button>'
content = content.replace(target_btn, replacement_btn)


# 3. Add modal HTML
modal_html = """
        <!-- Player Details Modal -->
        <div id="playerDetailsModal" class="modal-overlay">
            <div class="modal-content-large">
                <div class="modal-header">
                    <div class="modal-title">플레이어 상세 — 36690843045728256 (Shard 1)</div>
                    <i class="fa-solid fa-xmark" style="cursor: pointer; font-size: 20px; color: #94A3B8;" onclick="closeModal('playerDetailsModal')"></i>
                </div>
                
                <div class="modal-body">
                    <div class="page-lnb" style="margin-bottom: 0; padding-top: 16px; background: white; position: sticky; top: 0; z-index: 10;">
                        <div class="page-lnb-item active" onclick="switchDetailTab(this, 'tab-item')">아이템</div>
                        <div class="page-lnb-item" onclick="switchDetailTab(this, 'tab-poring')">포링</div>
                        <div class="page-lnb-item" onclick="switchDetailTab(this, 'tab-mail')">우편</div>
                        <div class="page-lnb-item" onclick="switchDetailTab(this, 'tab-payment')">결제</div>
                    </div>

                    <!-- Tab 1: 아이템 -->
                    <div id="tab-item" class="tab-content active">
                        <div class="form-card" style="box-shadow: none; border-color: #E2E8F0;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                                <div style="font-size: 15px; font-weight: 700;">재화/아이템 지급</div>
                                <select style="width: 120px; padding: 6px 12px; border-radius: 6px; border: 1px solid var(--border-color); outline: none;">
                                    <option>grant</option>
                                </select>
                            </div>
                            <button style="background: white; border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-bottom: 16px; cursor: pointer;">보상 추가</button>
                            <input type="text" placeholder="사유(필수)" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border-color); border-radius: 6px; margin-bottom: 16px; outline: none; font-size: 14px;">
                            <button style="background-color: var(--primary-blue); color: white; border: none; padding: 8px 24px; border-radius: 6px; font-weight: 600; cursor: pointer;">지급</button>
                        </div>
                        
                        <div style="border: 1px solid #FECACA; background-color: #FEF2F2; border-radius: 8px; padding: 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 14px; color: var(--text-gray);">로비 초기화(파괴적: 포링/알/케어/진화/외출 삭제)</div>
                            <button style="background-color: #FEE2E2; color: #EF4444; border: none; padding: 6px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;">로비 초기화</button>
                        </div>

                        <div style="border: 1px solid #FECACA; background-color: #FEF2F2; border-radius: 8px; padding: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 14px; color: var(--text-gray);">계정 전체 초기화(파괴적: 인벤토리·우편·출석·업적·상점 등 전체 삭제 → 신규 기본 지급 재지급)</div>
                            <button style="background-color: #FEE2E2; color: #EF4444; border: none; padding: 6px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;">계정 전체 초기화</button>
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding: 0 4px;">
                            <div style="font-size: 14px; font-weight: 700; color: var(--text-gray);">보유 아이템/재화 (15/15)</div>
                            <div style="display: flex; gap: 12px; align-items: center;">
                                <input type="text" placeholder="이름/ID 검색" style="padding: 6px 12px; border: 1px solid var(--border-color); border-radius: 20px; font-size: 13px; outline: none; width: 160px;">
                                <div style="display: flex; gap: 12px; font-size: 13px; font-weight: 600;">
                                    <span style="color: var(--primary-blue); background-color: #EFF6FF; padding: 2px 8px; border-radius: 4px;">전체</span>
                                    <span style="color: var(--text-gray); cursor: pointer;">유료</span>
                                    <span style="color: var(--text-gray); cursor: pointer;">무료</span>
                                    <span style="color: var(--text-gray); cursor: pointer;">일반</span>
                                </div>
                            </div>
                        </div>
                        
                        <div style="border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: white;">
                            <table class="data-table" style="background: white;">
                                <thead>
                                    <tr>
                                        <th style="width: 20%; background: white;">ItemID <i class="fa-solid fa-caret-up ml-1 text-slate-400"></i></th>
                                        <th style="width: 35%; background: white;">이름</th>
                                        <th style="width: 25%; background: white;">수량</th>
                                        <th style="width: 20%; background: white;">잠금</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="color: var(--primary-blue); font-weight: 600;">2</td>
                                        <td>Free_Zeny <span style="background-color: #DCFCE7; color: #16A34A; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-left: 4px;">무료</span></td>
                                        <td style="font-weight: 500;">100,000</td>
                                        <td>-</td>
                                    </tr>
                                    <tr>
                                        <td style="color: var(--primary-blue); font-weight: 600;">5</td>
                                        <td>Valhalla Pass <span style="background-color: #DCFCE7; color: #16A34A; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-left: 4px;">무료</span></td>
                                        <td style="font-weight: 500;">1</td>
                                        <td>-</td>
                                    </tr>
                                    <tr>
                                        <td style="color: var(--primary-blue); font-weight: 600;">8</td>
                                        <td>Poring_Exp <span style="background-color: #DCFCE7; color: #16A34A; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-left: 4px;">무료</span></td>
                                        <td style="font-weight: 500;">500</td>
                                        <td>-</td>
                                    </tr>
                                    <tr>
                                        <td style="color: var(--primary-blue); font-weight: 600;">101</td>
                                        <td style="color: var(--text-gray);">Poring Egg</td>
                                        <td style="font-weight: 500;">4</td>
                                        <td>-</td>
                                    </tr>
                                    <tr>
                                        <td style="color: var(--primary-blue); font-weight: 600;">5001</td>
                                        <td style="color: var(--text-gray);">Likability_Item_1</td>
                                        <td style="font-weight: 500;">5</td>
                                        <td>-</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Tab 2: 포링 -->
                    <div id="tab-poring" class="tab-content">
                        <div style="font-size: 13px; font-weight: 700; color: var(--text-gray); margin-bottom: 8px;">포링 — 전 슬롯 (1)</div>
                        <div style="border: 1px solid var(--border-color); border-radius: 6px; padding: 12px 16px; margin-bottom: 24px; font-size: 14px; background: white;">
                            <span style="color: var(--text-gray);">Slot 1</span> &nbsp;&nbsp; <span style="color: var(--primary-blue); font-weight: 600;">PoringID 1</span> &nbsp;&nbsp; <span style="color: var(--text-gray);">Exp 0</span>
                        </div>

                        <div style="font-size: 13px; font-weight: 700; color: var(--text-gray); margin-bottom: 8px;">케어 상태</div>
                        <div style="display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap;">
                            <div style="border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; font-size: 13px; color: var(--text-dark); background: white;">[S1] 만족도: 6000</div>
                            <div style="border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; font-size: 13px; color: var(--text-dark); background: white;">[S1] 포만도: 6000</div>
                            <div style="border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; font-size: 13px; color: var(--text-dark); background: white;">[S1] 청결도: 6000</div>
                            <div style="border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; font-size: 13px; color: var(--text-dark); background: white;">[S1] 체력: 6000</div>
                            <div style="border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 12px; font-size: 13px; color: var(--text-dark); background: white;">[S1] 건강: 10000</div>
                        </div>

                        <div style="font-size: 13px; font-weight: 700; color: var(--text-gray); margin-bottom: 4px;">알 (0) · 활성 버프 0개</div>
                        <div style="font-size: 14px; color: #94A3B8; margin-bottom: 24px;">보유 알 없음</div>

                        <div class="form-card" style="padding: 20px; margin-bottom: 16px; box-shadow: none;">
                            <div style="font-size: 13px; font-weight: 700; margin-bottom: 12px;">포링 경험치 보정</div>
                            <div style="display: flex; gap: 12px; align-items: flex-end;">
                                <div>
                                    <div style="font-size: 12px; color: var(--text-dark); margin-bottom: 4px;">Slot</div>
                                    <input type="text" style="width: 60px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px;">
                                </div>
                                <div>
                                    <div style="font-size: 12px; color: var(--text-dark); margin-bottom: 4px;">값</div>
                                    <input type="text" style="width: 100px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px;">
                                </div>
                                <div>
                                    <div style="font-size: 12px; color: var(--text-dark); margin-bottom: 4px;">set/add</div>
                                    <input type="text" style="width: 100px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px;">
                                </div>
                                <div style="flex: 1;">
                                    <input type="text" placeholder="사유(필수)" style="width: 100%; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px;">
                                </div>
                                <button style="background-color: #818CF8; color: white; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 600; font-size: 13px; cursor: pointer;">보정</button>
                            </div>
                        </div>

                        <div class="form-card" style="padding: 20px; margin-bottom: 24px; box-shadow: none;">
                            <div style="font-size: 13px; font-weight: 700; margin-bottom: 12px;">케어 상태 보정 (빈사 복구)</div>
                            <div style="display: flex; gap: 12px; margin-bottom: 12px;">
                                <div>
                                    <div style="font-size: 12px; color: var(--text-dark); margin-bottom: 4px;">Slot</div>
                                    <input type="text" value="1" style="width: 80px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px;">
                                </div>
                                <div>
                                    <div style="font-size: 12px; color: var(--text-dark); margin-bottom: 4px;">항목</div>
                                    <select style="width: 120px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px;">
                                        <option selected>4</option>
                                    </select>
                                </div>
                                <div>
                                    <div style="font-size: 12px; color: var(--text-dark); margin-bottom: 4px;">값(0~10000)</div>
                                    <input type="text" value="10000" style="width: 120px; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px;">
                                </div>
                            </div>
                            <input type="text" placeholder="사유(필수)" style="width: 100%; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; outline: none; font-size: 13px; margin-bottom: 12px;">
                            <button style="background-color: #818CF8; color: white; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 600; font-size: 13px; cursor: pointer;">보정</button>
                        </div>

                        <div style="font-size: 13px; color: var(--text-gray); text-decoration: underline; cursor: pointer; padding-bottom: 16px;">고급 보정 열기 (진화/포링교체/알잠금/호감도/도감)</div>
                    </div>

                    <!-- Tab 3: 우편 -->
                    <div id="tab-mail" class="tab-content">
                        <div style="border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: white;">
                            <table class="data-table" style="margin-bottom: 0;">
                                <thead>
                                    <tr>
                                        <th style="width: 10%; background: white;">ID</th>
                                        <th style="width: 30%; background: white;">제목</th>
                                        <th style="width: 20%; background: white;">발송</th>
                                        <th style="width: 15%; background: white;">보상</th>
                                        <th style="width: 15%; background: white;">상태</th>
                                        <th style="width: 10%; background: white;">관리</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="6" style="text-align: center; padding: 60px 40px; color: #94A3B8; font-size: 14px; font-weight: 500;">우편이 없습니다.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Tab 4: 결제 -->
                    <div id="tab-payment" class="tab-content">
                        <div style="border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; background: white;">
                            <table class="data-table" style="margin-bottom: 0;">
                                <thead>
                                    <tr>
                                        <th style="width: 15%; background: white;">일시</th>
                                        <th style="width: 20%; background: white;">상품(Tid)</th>
                                        <th style="width: 10%; background: white;">수량</th>
                                        <th style="width: 20%; background: white;">비용(유료/무료)</th>
                                        <th style="width: 10%; background: white;">상태</th>
                                        <th style="width: 10%; background: white;">결과</th>
                                        <th style="width: 15%; background: white;">TrxId</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="7" style="text-align: center; padding: 60px 40px; color: #94A3B8; font-size: 14px; font-weight: 500;">결제 이력이 없습니다.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <script>
        function switchDetailTab(element, tabId) {
            document.querySelectorAll('#playerDetailsModal .page-lnb-item').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('#playerDetailsModal .tab-content').forEach(el => el.classList.remove('active'));
            
            element.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }
        </script>
"""

# 4. Inject modal script right before closing body
if 'playerDetailsModal' not in content:
    content = content.replace('</body>', modal_html + '\n</body>')

with open('user_management.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added Player Details Modal correctly.")
