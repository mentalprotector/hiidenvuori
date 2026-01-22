import os
import re
from bs4 import BeautifulSoup

def debug_search(file_name):
    if not os.path.exists(file_name): return

    with open(file_name, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False
    
    # 1. Удаление по картинке (самый надежный способ)
    img_src_part = "tph63pnu86scoko8s8k8gckggwss4s"
    
    for img in soup.find_all("img"):
        if img_src_part in img.get("src", ""):
            print(f"Found Shatry Image in {file_name}")
            parent_li = img.find_parent("li")
            if parent_li:
                print("Deleting LI container...")
                parent_li.decompose()
                modified = True
    
    # 2. Удаление альбома
    album_link = soup.find("a", href=re.compile("photoalbums/907027"))
    if album_link:
        print(f"Found Album Link in {file_name}")
        album_item = album_link.find_parent(class_="albums__item")
        if album_item:
            print("Deleting Album item...")
            album_item.decompose()
            modified = True

    if modified:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Saved {file_name}")

debug_search("index.html")
debug_search("uslugi.html")
debug_search("photoalbums.html")