import os
import glob
import re

# 1. Rename existing index.html to prereg.html
if os.path.exists('index.html') and not os.path.exists('prereg.html'):
    os.rename('index.html', 'prereg.html')

# 2. Update navigation links in all HTML files
html_files = glob.glob('*.html')
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change "index.html" to "prereg.html" for the "사전예약 관리" menu
    content = content.replace("location.href='index.html'\">사전예약 관리", "location.href='prereg.html'\">사전예약 관리")
    
    # Make the logo click go to index.html (the new dashboard)
    if 'class="logo-text">Admin Tools</div>' in content:
        content = content.replace('class="logo-text">Admin Tools</div>', 'class="logo-text" style="cursor:pointer;" onclick="location.href=\'index.html\'">Admin Tools</div>')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Renamed index.html to prereg.html and updated LNBs.")
