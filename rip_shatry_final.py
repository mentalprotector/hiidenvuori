import os
import re
from bs4 import BeautifulSoup

# Files to process
html_files = ["hiidenvuori/index.html", "hiidenvuori/uslugi.html", "hiidenvuori/photoalbums.html"]

def clean_shatry(file_path):
    if not os.path.exists(file_path): return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    modified = False

    # 1. Удаление карточек с Шатрами по картинке (find_all!)
    img_src = "assets/img/tph63pnu86scoko8s8k8gckggwss4s"
    
    for img in soup.find_all("img", src=img_src):
        # Ищем родительский элемент списка (карточку)
        # Пробуем найти ближайший li
        card = img.find_parent("li")
        if card:
            card.decompose()
            modified = True
            print(f"Removed 'Shatry' card from {file_path}")
        else:
            print(f"Found image in {file_path} but no parent LI found!")

    # 2. Удаление альбома "Глэмпинг"
    album_link = soup.find("a", href=re.compile("photoalbums/907027"))
    if album_link:
        album_container = album_link.find_parent(class_="albums__item")
        if album_container:
            album_container.decompose()
            modified = True
            print(f"Removed 'Glamping' album from {file_path}")

    # 3. Правка FAQ (index.html)
    for p in soup.find_all("p"):
        text = p.get_text()
        if "снять шатёр" in text:
            # Ручная правка текста
            new_text = text.replace(", снять шатёр а", "").replace("снять шатёр", "")
            new_text = re.sub(r'\s+', ' ', new_text).strip()
            new_text = new_text.replace(" а ", " ") 
            new_text = new_text.replace(" ,", ",")
            p.string = new_text
            modified = True
            print(f"Fixed FAQ in {file_path}")

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))

for f in html_files:
    clean_shatry(f)