import os
import re

img_dir = "assets/img"
html_files = [
    "index.html", "uslugi.html", "razmeshhenie.html", "stoyanka-dlya-avtodomov.html",
    "contacts.html", "agreement.html", "privacy.html", "aktivnyj-otdykh.html",
    "comment.html", "magazin-kafe-saha.html", "rules.html", "transfer-v-ruskealu.html"
]

def final_cleanup(content, is_index=False):
    # 1. Global .png/.jpg to .webp replacement for assets/img/
    # This covers favicons and Palatka1.png
    content = re.sub(r"assets/img/([a-zA-Z0-9_-]+)\.(png|jpg|jpeg)", r"assets/img/\1.webp", content)
    
    # 2. Specific replacements for index.html gallery as requested
    if is_index:
        # mziqpz0... -> naves.webp
        content = re.sub(r"assets/img/mziqpz0enhwc8kkg0s8c088wkoswg0(\.webp)?", "assets/img/naves.webp", content)
        # np3wb8... -> palatka_large.webp
        content = re.sub(r"assets/img/np3wb8n21r4kwg4kc4kkoso4ggg880(\.webp)?", "assets/img/palatka_large.webp", content)
        
    # 3. Ensure no siteapi links remain
    content = re.sub(r"//i\.siteapi\.org/[^\"'\s]*/([a-z0-9]{20,})", r"assets/img/\1.webp", content)
    
    return content

for html_file in html_files:
    if not os.path.exists(html_file):
        continue
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = final_cleanup(content, is_index=(html_file == "index.html"))
    
    if new_content != content:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {html_file}")

print("Cleanup done.")
