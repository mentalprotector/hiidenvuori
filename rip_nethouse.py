import os
from bs4 import BeautifulSoup
import re

# Files to process
html_files = [f for f in os.listdir(".") if f.endswith(".html")]

def clean_nethouse(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    modified = False

    # 1. Remove Nethouse logo and links in footer
    # Usually inside <div class="project-info"> or adjacent to it
    footer_logo = soup.find(id="project-info")
    if footer_logo:
        footer_logo.decompose()
        modified = True
    
    nh_logo_link = soup.find(id="nh-logo")
    if nh_logo_link:
        nh_logo_link.decompose()
        modified = True

    # 2. Remove "Create site for free" links (often in footer)
    for a in soup.find_all("a", href=re.compile(r"nethouse\.ru")):
        # Check if it's a generic Nethouse link
        if "Создать" in a.get_text() or "Конструктор" in a.get_text() or "nethouse" in a.get_text().lower():
            # If it has a parent wrapper like 'project-info__link-wrap', remove parent
            parent = a.find_parent(class_="project-info__link-wrap")
            if parent:
                parent.decompose()
            else:
                a.decompose()
            modified = True

    # 3. Remove "target=Nethouse.ru" and similar titles
    for tag in soup.find_all(attrs={"target": "Nethouse.ru"}):
        del tag["target"]
        modified = True
    
    for tag in soup.find_all(title=re.compile(r"Nethouse", re.I)):
        del tag["title"]
        modified = True

    # 4. Remove any meta tags mentioning Nethouse
    for meta in soup.find_all("meta", content=re.compile(r"Nethouse", re.I)):
        meta.decompose()
        modified = True

    if modified:
        print(f"Removed Nethouse mentions from {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))

# Process HTMLs
for f in html_files:
    clean_nethouse(f)

# 5. Clean JS translate file
js_path = os.path.join("assets", "js", "translate.js")
if os.path.exists(js_path):
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()
    
    if "Nethouse" in js_content:
        # Replace Nethouse with a generic name or empty string in common strings
        js_content = js_content.replace("Nethouse", "Наш сервис")
        # Also hide specific banner texts if they are plain strings
        js_content = js_content.replace("Сайт создан на платформе Наш сервис. Хотите такой же?", "")
        
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"Cleaned {js_path}")

print("Nethouse cleanup complete.")
