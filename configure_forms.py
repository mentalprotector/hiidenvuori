import os
import re
from bs4 import BeautifulSoup

# Config
NEW_EMAIL = "mail@hiidenvuori.ru"
FORMSUBMIT_ACTION = f"https://formsubmit.co/{NEW_EMAIL}"
# Используем относительный путь для универсальности, или абсолютный если sslip
THANKYOU_PAGE = "https://hiidenvuori.94.140.224.220.sslip.io/thankyou.html" 

def patch_forms_advanced(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False
    
    forms = soup.find_all("form")
    for form in forms:
        if form.find("input"): 
            form["action"] = FORMSUBMIT_ACTION
            form["method"] = "POST"
            
            # Удаляем старые скрытые поля
            for hidden in form.find_all("input", type="hidden"):
                if hidden.get("name", "").startswith("_"):
                    hidden.decompose()

            # Добавляем новые
            # name="_next"
            next_input = soup.new_tag("input", attrs={"type": "hidden", "name": "_next", "value": THANKYOU_PAGE})
            form.append(next_input)
            
            # name="_subject"
            sub_input = soup.new_tag("input", attrs={"type": "hidden", "name": "_subject", "value": "Новая заявка (Хийденвуори)"})
            form.append(sub_input)
            
            # name="_captcha"
            cap_input = soup.new_tag("input", attrs={"type": "hidden", "name": "_captcha", "value": "false"})
            form.append(cap_input)

            # name="_template"
            tpl_input = soup.new_tag("input", attrs={"type": "hidden", "name": "_template", "value": "table"})
            form.append(tpl_input)

            if form.get("id") and not form["id"].endswith("_static"):
                form["id"] = form["id"] + "_static"
            
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Configured FormSubmit in {file_path}")

html_files = [f for f in os.listdir("hiidenvuori") if f.endswith(".html")]
for f in html_files:
    full_path = os.path.join("hiidenvuori", f)
    patch_forms_advanced(full_path)