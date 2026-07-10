import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Poppins with Pretendard CDN
content = content.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">',
    '<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css" />'
)

# Add tailwind config script to set default font
tailwind_config = """
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Pretendard Variable"', 'Pretendard', 'sans-serif'],
                        pretendard: ['"Pretendard Variable"', 'Pretendard', 'sans-serif']
                    }
                }
            }
        }
    </script>"""
    
content = content.replace('<script src="https://cdn.tailwindcss.com"></script>', tailwind_config)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html to use Pretendard font.")
