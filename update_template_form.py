import os

with open('template_form.html', 'r', encoding='utf-8') as f:
    template_form_html = f.read()

with open('notice_form.html', 'r', encoding='utf-8') as f:
    notice_form_html = f.read()

# 1. Extract the top part of template_form.html (up to <div class="form-group-title">언어별 정보</div>)
top_part = template_form_html.split('<div class="form-group-title">언어별 정보</div>')[0]

# 2. Extract the bottom part of notice_form.html (from <div class="form-group-title">언어별 정보</div> to the end)
bottom_part = notice_form_html.split('<div class="form-group-title">언어별 정보</div>')[1]

# 3. Clean up bottom_part specifics for template:
# In bottom_part, we need to change location.href='notice.html' to location.href='template.html'
bottom_part = bottom_part.replace("location.href='notice.html'", "location.href='template.html'")

# Combine them
new_template_form_html = top_part + '<div class="form-group-title">언어별 정보</div>\n' + bottom_part

with open('template_form.html', 'w', encoding='utf-8') as f:
    f.write(new_template_form_html)

print("template_form.html updated.")
