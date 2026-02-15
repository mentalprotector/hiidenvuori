import re
import os

def localise_images(content):
    # Regex to find any i.siteapi.org link and extract the last part (the hash)
    # Match //i.siteapi.org/.../HASH
    # Hash is usually alphanumeric, at least 20 chars
    pattern = re.compile(r"//i\.siteapi\.org/[^\"'\s]*/([a-z0-9]{20,})")
    content = pattern.sub(r"assets/img/\1", content)
    
    # Handle cases where it is just the hash without the full path
    # content = re.sub(r"//i\.siteapi\.org/[^\"'\s]+", "assets/img/placeholder.png", content)
    
    return content

for filename in ["index.html", "uslugi.html", "razmeshhenie.html", "stoyanka-dlya-avtodomov.html"]:
    if not os.path.exists(filename): continue
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = localise_images(content)
    
    if new_content != content:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Localised images in {filename}")
