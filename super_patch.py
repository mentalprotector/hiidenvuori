import os
import re
from bs4 import BeautifulSoup
from PIL import Image

# Config
DOMAIN = "https://xn--b1aigpbrd8abgk.xn--p1ai" # хийденвуори.рф
PHONE = "+79212205533"

# 1. Tags
SCHEMA_ORG = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LodgingBusiness",
  "name": "Хийденвуори",
  "url": "https://xn--b1aigpbrd8abgk.xn--p1ai",
  "telephone": "+79212205533",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "п. Хийденсельга",
    "addressRegion": "Республика Карелия",
    "addressCountry": "RU"
  }
}
</script>
"""

OG_TAGS = """
<!-- Preconnect -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="Хийденвуори | Туристическое пространство">
<meta property="og:description" content="Отдых в Карелии на берегу Ладоги. Кемпинг, прокат, природа.">
"""

def optimize_images():
    img_dir = os.path.join("assets", "img")
    if not os.path.exists(img_dir): return
    
    print("Optimizing images to WebP...")
    for filename in os.listdir(img_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(img_dir, filename)
            webp_path = os.path.splitext(path)[0] + ".webp"
            
            if not os.path.exists(webp_path):
                try:
                    with Image.open(path) as img:
                        img.save(webp_path, "WEBP", quality=80)
                    # We don't delete original to keep HTML working for now, 
                    # but we could replace src in HTML later.
                except Exception as e:
                    print(f"Failed to convert {filename}: {e}")

def patch_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    modified = False

    # A. Add Tags to Head
    head = soup.head
    if head:
        if "application/ld+json" not in str(head):
            head.append(BeautifulSoup(SCHEMA_ORG, "html.parser"))
            head.append(BeautifulSoup(OG_TAGS, "html.parser"))
            modified = True

    # B. Lazy Loading
    for img in soup.find_all("img"):
        if not img.get("loading"):
            img["loading"] = "lazy"
            modified = True

    # C. Clickable Phones
    for text_node in soup.find_all(string=re.compile(r'\+7\s?\(921\)\s?220-55-33')):
        parent = text_node.parent
        if parent.name != 'a':
            new_tag = soup.new_tag("a", href=f"tel:{PHONE}")
            new_tag.string = str(text_node)
            text_node.replace_with(new_tag)
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Patched {file_path}")

# Run
optimize_images()
html_files = [f for f in os.listdir(".") if f.endswith(".html")]
for f in html_files:
    patch_html(f)

# 4. 404 Page
if not os.path.exists("404.html"):
    with open("404.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>404 - Страница не найдена</title><style>body{font-family:sans-serif;text-align:center;padding:100px;}a{color:#3384BF;}</style></head><body><h1>404</h1><p>Упс! Такой страницы нет.</p><a href='/'>Вернуться на главную</a></body></html>")

print("All tasks complete.")