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

    # 1. Удаление карточек с услугой "Шатры"
    # Ищем по уникальному описанию: "Мебелированы кроватью" или "Предоставляем клиентам шатры"
    # Nethouse может использовать разные классы, но текст внутри <p> должен быть.
    
    # Ключевые фразы, которые точно идентифицируют блок шатров
    keywords = ["Мебелированы кроватью", "Предоставляем клиентам шатры", "снять шатёр"]

    # Проходим по всем элементам, содержащим текст
    for element in soup.find_all(string=True):
        if any(k in element for k in keywords):
            # Если это FAQ (вопрос-ответ), мы правим текст, а не удаляем блок
            if "снять шатёр" in element:
                # Это FAQ в index.html: "можно остановиться с автодомом, снять шатёр а или приехать"
                new_text = element.replace(", снять шатёр а", "").replace("снять шатёр", "")
                element.replace_with(new_text)
                modified = True
            else:
                # Это карточка услуги. Нужно удалить весь элемент списка.
                # Идем вверх до li
                parent_li = element.find_parent("li")
                if parent_li:
                    parent_li.decompose()
                    modified = True
                else:
                    # Если li нет (вдруг структура другая), пробуем найти карточку
                    parent_card = element.find_parent(class_="cards__item")
                    if parent_card:
                        parent_card.decompose()
                        modified = True

    # 2. Удаление альбома "Глэмпинг"
    # Ищем ссылку на альбом 907027
    album_link = soup.find("a", href=re.compile("photoalbums/907027"))
    if album_link:
        # Удаляем контейнер альбома (обычно div.albums__item)
        album_container = album_link.find_parent(class_="albums__item")
        if album_container:
            album_container.decompose()
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Cleaned {file_path}")

for f in html_files:
    clean_shatry(f)
