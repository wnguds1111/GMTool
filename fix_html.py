import re

with open('exact_sidebar.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'(href|src)="(/_next/[^"]+)"', r'\1="https://stage-admin.mygnjoy.com\2"', html)
html = html.replace('href="/ko/', 'href="https://stage-admin.mygnjoy.com/ko/')
html = html.replace('href="/favicon', 'href="https://stage-admin.mygnjoy.com/favicon')
# Add FontAwesome since it uses fa-solid classes
if '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome' not in html:
    html = html.replace('</head>', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
