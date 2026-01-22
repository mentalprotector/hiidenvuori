import os
from bs4 import BeautifulSoup

html_files = [f for f in os.listdir("hiidenvuori") if f.endswith(".html")]

LINK_HTML = """<a class="nh-topbar-link nh-topbar-link__font nh-topbar-link__font--14 nh-topbar-link__font--none nh-topbar-link__font--paragraph nh-topbar-link__font--underline-2" href="aktivnyj-otdykh.html" style="--nh-topbar-link-color:#102748;--nh-topbar-link-hover:#3384BF;--nh-topbar-link-active:#3384BF;" target="_parent">
                Активный отдых
            </a>"""

BURGER_LINK_HTML = """<li class="nh-burger-menu__links-item">
<a class="nh-burger-menu__link" href="aktivnyj-otdykh.html" style="--item-color: #FFFFFF; --item-hover: #3384BF;" target="_parent">
                                            Активный отдых
                                        </a>
</li>"""

for file_name in html_files:
    file_path = os.path.join("hiidenvuori", file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        # Используем html.parser, он не добавляет html/body теги, если фрагмент
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False

    # 1. Top Bar
    camping_link = soup.find("a", href="stoyanka-dlya-avtodomov.html", class_="nh-topbar-link")
    if camping_link:
        next_sibling = camping_link.find_next_sibling("a")
        # Проверяем, есть ли уже ссылка (чтобы не дублировать)
        if not next_sibling or "aktivnyj-otdykh.html" not in next_sibling.get("href", ""):
            # Создаем элемент из строки
            new_link_soup = BeautifulSoup(LINK_HTML, "html.parser")
            new_link_tag = new_link_soup.find("a")
            if new_link_tag:
                camping_link.insert_after(new_link_tag)
                modified = True
                print(f"Added TopBar link to {file_name}")

    # 2. Burger Menu
    burger_camping_link = soup.find("a", href="stoyanka-dlya-avtodomov.html", class_="nh-burger-menu__link")
    if burger_camping_link:
        parent_li = burger_camping_link.find_parent("li")
        if parent_li:
            next_li = parent_li.find_next_sibling("li")
            
            new_li_soup = BeautifulSoup(BURGER_LINK_HTML, "html.parser")
            new_li_tag = new_li_soup.find("li")

            if new_li_tag:
                # Если следующий li пустой, заменяем
                if next_li and not next_li.text.strip():
                    next_li.replace_with(new_li_tag)
                    modified = True
                    print(f"Replaced empty Burger li in {file_name}")
                # Если следующего нет или он не "Активный отдых", добавляем
                elif not next_li or (next_li.find("a") and "aktivnyj-otdykh.html" not in next_li.find("a").get("href", "")):
                     parent_li.insert_after(new_li_tag)
                     modified = True
                     print(f"Added Burger li to {file_name}")

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))

print("Menu injection done.")