import os
import re
from bs4 import BeautifulSoup

# Files to process
html_files = ["hiidenvuori/index.html", "hiidenvuori/uslugi.html", "hiidenvuori/photoalbums.html"]

def clean_shatry(file_path):
    if not os.path.exists(file_path): return

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False

    # 1. Удаление карточек с текстом "Предоставляем клиентам шатры"
    # Текст внутри <p>, карточка обычно выше.
    for p in soup.find_all("p"):
        if "Предоставляем клиентам шатры" in p.get_text():
            # Ищем родительскую карточку. В Nethouse это часто li.nh-features__item или div.cards__item
            # В данном случае, судя по структуре, это может быть div внутри списка.
            # Попробуем найти ближайший li или div с классом item
            
            # Вариант 1: Features item
            card = p.find_parent("li", class_="nh-features__item")
            if card:
                card.decompose()
                modified = True
                continue
            
            # Вариант 2: Generic Cards item
            card = p.find_parent(class_="cards__item")
            if card:
                card.decompose()
                modified = True
                continue

    # 2. Правка текста в FAQ (index.html)
    # "снять шатёр а или приехать" -> "или приехать"
    for p in soup.find_all("p"):
        text = p.get_text()
        if "снять шатёр" in text:
            # Заменяем фразу аккуратно
            new_text = text.replace(", снять шатёр а", "").replace("снять шатёр", "")
            # Если остались лишние запятые/пробелы
            new_text = new_text.replace("  ", " ").replace(" ,", ",")
            p.string = new_text
            modified = True

    # 3. Удаление альбома (photoalbums.html)
    # Ищем ссылку
    album_link = soup.find("a", href=re.compile("photoalbums/907027"))
    if album_link:
        # Удаляем родительский контейнер альбома
        album_item = album_link.find_parent(class_="albums__item")
        if album_item:
            album_item.decompose()
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Cleaned {file_path}")

for f in html_files:
    clean_shatry(f)
