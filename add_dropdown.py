import os

with open('mail_all_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Dropdown CSS
dropdown_css = """
        .dropdown-menu {
            position: absolute; top: 100%; left: 0; right: 0; background: var(--white);
            border: 1px solid var(--border-color); border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10; max-height: 200px; overflow-y: auto; display: none; margin-top: 4px;
        }
        .dropdown-menu.show { display: block; }
        .dropdown-item {
            display: flex; justify-content: space-between; align-items: center;
            padding: 8px 12px; cursor: pointer; transition: background 0.2s;
        }
        .dropdown-item:hover { background-color: var(--active-bg); }
        .dropdown-item-text { font-size: 14px; color: var(--text-dark); }
"""
if '.dropdown-menu {' not in content:
    content = content.replace('</style>', dropdown_css + '    </style>')

# 2. Add Dropdown HTML to the empty input wrap
old_empty_input = """<div class="reward-input-wrap">
                            <input type="text" class="form-control" placeholder="아이템 검색 / ID">
                        </div>"""

new_empty_input = """<div class="reward-input-wrap">
                            <input type="text" class="form-control" placeholder="아이템 검색 / ID" onclick="toggleDropdown(this)" onfocus="toggleDropdown(this)" readonly style="cursor: pointer; background-color: var(--white);">
                            <div class="dropdown-menu">
                                <div class="dropdown-item" onclick="selectItem(this, '1 Paid_Zeny', 'paid')">
                                    <span class="dropdown-item-text">1 Paid_Zeny</span>
                                    <span class="badge paid">유료</span>
                                </div>
                                <div class="dropdown-item" onclick="selectItem(this, '2 Free_Zeny', 'free')">
                                    <span class="dropdown-item-text">2 Free_Zeny</span>
                                    <span class="badge free">무료</span>
                                </div>
                                <div class="dropdown-item" onclick="selectItem(this, '3 Paid_Dia', 'paid')">
                                    <span class="dropdown-item-text">3 Paid_Dia</span>
                                    <span class="badge paid">유료</span>
                                </div>
                                <div class="dropdown-item" onclick="selectItem(this, '4 Free_Dia', 'free')">
                                    <span class="dropdown-item-text">4 Free_Dia</span>
                                    <span class="badge free">무료</span>
                                </div>
                                <div class="dropdown-item" onclick="selectItem(this, '5 Valhalla Pass', 'free')">
                                    <span class="dropdown-item-text">5 Valhalla Pass</span>
                                    <span class="badge free">무료</span>
                                </div>
                                <div class="dropdown-item" onclick="selectItem(this, '6 Nickname Change Ticket', 'free')">
                                    <span class="dropdown-item-text">6 Nickname Change Ticket</span>
                                    <span class="badge free">무료</span>
                                </div>
                            </div>
                        </div>"""
content = content.replace(old_empty_input, new_empty_input)

# 3. Add JS functions
dropdown_js = """
        function toggleDropdown(input) {
            // Close all others first
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (menu !== input.nextElementSibling) {
                    menu.classList.remove('show');
                }
            });
            const menu = input.nextElementSibling;
            if(menu && menu.classList.contains('dropdown-menu')) {
                menu.classList.toggle('show');
            }
        }

        function selectItem(element, text, type) {
            const wrap = element.closest('.reward-input-wrap');
            const input = wrap.querySelector('input');
            const menu = wrap.querySelector('.dropdown-menu');
            
            // Set value
            input.value = text;
            
            // Remove existing badge if any
            const existingBadge = wrap.querySelector('.badge');
            if (existingBadge) {
                existingBadge.remove();
            }
            
            // Add new badge
            const badge = document.createElement('span');
            badge.className = `badge ${type}`;
            badge.textContent = type === 'paid' ? '유료' : '무료';
            wrap.appendChild(badge);
            
            // Hide menu
            menu.classList.remove('show');
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.reward-input-wrap')) {
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
"""
if 'function toggleDropdown' not in content:
    content = content.replace('</script>', dropdown_js + '    </script>')

with open('mail_all_form.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dropdown logic added to mail_all_form.html")
