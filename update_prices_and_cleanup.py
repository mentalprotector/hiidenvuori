import os
import re
from bs4 import BeautifulSoup

PRICE_MAP = {
    "600,00 руб./сутки за 1 чел.": "700,00 руб./сутки за 1 чел.",
    "1400,00 руб./сутки": "1500,00 руб./сутки",
    "1800,00 руб./сутки": "2000,00 руб./сутки",
    "Для проживающих — бесплатно. Душ — 15 минут в день. Дополнительное время можно взять за отдельную плату.": 
    "Для проживающих душ платный — 350 руб. за 15 мин. Каждые следующие 10 мин. — 50 руб."
}

FAQ_OLD_TEXT_PART = "Для проживающих — бесплатно. Душ — 15 минут в день"
FAQ_NEW_TEXT = "Для проживающих душ платный — 350 руб. за 15 мин. Каждые следующие 10 мин. — 50 руб."

SHATRY_KEYWORD = "Мебелированы кроватью"

html_files = [f for f in os.listdir("hiidenvuori") if f.endswith(".html")]

for file_name in html_files:
    file_path = os.path.join("hiidenvuori", file_name)
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False
    
    # 1. Update Prices and FAQ (Exact)
    for element in soup.find_all(string=True):
        for old_text, new_text in PRICE_MAP.items():
            if old_text in element:
                updated_text = element.replace(old_text, new_text)
                element.replace_with(updated_text)
                modified = True
                print(f"Updated text in {file_name}")

    # 1.1 Update FAQ (Flexible)
    for element in soup.find_all(string=True):
        if FAQ_OLD_TEXT_PART in element and FAQ_NEW_TEXT not in element:
             new_text = element.replace("Для проживающих — бесплатно. Душ — 15 минут в день. Дополнительное время можно взять за отдельную плату.", FAQ_NEW_TEXT)
             if new_text != element:
                element.replace_with(new_text)
                modified = True
                print(f"Updated FAQ (Flexible) in {file_name}")

    # 2. Remove Shatry Card
    for element in soup.find_all(string=lambda t: t and SHATRY_KEYWORD in t):
        card = element.find_parent("li")
        if card:
            card.decompose()
            modified = True
            print(f"Removed Shatry card in {file_name}")

    # 3. Remove Glamping Album
    album_link = soup.find("a", href=re.compile("photoalbums/907027"))
    if album_link:
        album_container = album_link.find_parent(class_="albums__item")
        if album_container:
            album_container.decompose()
            modified = True
            print(f"Removed Glamping album in {file_name}")

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))

print("Done.")
