import os

with open('rofactory.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove tailwind-init.js
content = content.replace('<script src="tailwind-init.js"></script>', '')

# 2. Change Admin link to notice.html
content = content.replace('href="admin.html"', 'href="notice.html"')

# 3. Add QnA section at the bottom of the card
qna_html = """
            <!-- QnA Section -->
            <div class="mt-8 pt-8 border-t border-slate-200/60 text-left">
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-10 h-10 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center text-lg shadow-inner">❓</div>
                    <div class="text-[18px] font-extrabold text-slate-800">주요 질의 사항 <span class="text-[13px] font-semibold text-slate-500 ml-2">(API 수급 필요 리스트)</span></div>
                </div>
                <div class="flex flex-col gap-3">
                    <div class="p-4 bg-white/60 border border-white/80 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                        <div class="text-[14px] font-bold text-slate-700">1. 우편 관리 > 등록 템플릿 > 조회 API 수급 필요</div>
                    </div>
                    <div class="p-4 bg-white/60 border border-white/80 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                        <div class="text-[14px] font-bold text-slate-700">2. 단건 우편 발송의 건 이력 조회 API 수급 필요</div>
                    </div>
                </div>
            </div>
"""

# Insert right before the closing divs of the card
# Looking at rofactory.html:
#                 <!-- Item 6: Policy Checklist -->
#                 ...
#             </div>
#         </div>
#     </div>

insert_target = "            </div>\n        </div>\n    </div>"
if insert_target in content:
    content = content.replace(insert_target, "            </div>\n" + qna_html + "        </div>\n    </div>")
else:
    # Use regex or find to be safer
    idx = content.rfind('</div>\n        </div>\n    </div>')
    if idx != -1:
        content = content[:idx] + "</div>\n" + qna_html + "        </div>\n    </div>\n" + content[idx+32:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created new index.html with Tailwind UI and QnA section.")
