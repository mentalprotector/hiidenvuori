import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

def remove_gallery_stuff(content):
    # 1. Remove <li> blocks containing photoalbums.html (Burger Menu and Footer)
    # <li class="nh-burger-menu__links-item"><a class="nh-burger-menu__link" href="photoalbums.html" ...> Фотогалерея </a></li>
    content = re.sub(r'<li[^>]*>\s*<a[^>]*href="photoalbums\.html"[^>]*>.*?</a>\s*</li>', '', content, flags=re.IGNORECASE | re.DOTALL)
    
    # 2. Remove Topbar links
    # <a class="nh-topbar-link ..." href="photoalbums.html" ...> Галерея </a>
    content = re.sub(r'<a[^>]*href="photoalbums\.html"[^>]*>.*?</a>', '', content, flags=re.IGNORECASE | re.DOTALL)
    
    # 3. Remove CTA button blocks leading to photoalbums.html
    # <div class="nh-cta__btn-wrapper ..."> <a ... href="photoalbums.html" ...>Смотреть все фото</a> </div>
    content = re.sub(r'<div class="nh-cta__btn-wrapper[^"]*">\s*<a[^>]*href="photoalbums\.html"[^>]*>.*?</a>\s*</div>', '', content, flags=re.IGNORECASE | re.DOTALL)

    return content

for filename in html_files:
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        old_content = f.read()
    
    new_content = remove_gallery_stuff(old_content)
    
    if old_content != new_content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {filename}")

# Final check for any remaining occurrences of 'photoalbums.html'
