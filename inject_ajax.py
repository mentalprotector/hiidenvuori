import os
import glob

# Удаляем thankyou.html, так как клиент захотел AJAX
if os.path.exists("hiidenvuori/thankyou.html"):
    os.remove("hiidenvuori/thankyou.html")
    print("Deleted thankyou.html")

script_tag = '<script src="assets/js/form-ajax.js"></script>'

html_files = glob.glob("hiidenvuori/*.html")

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Проверяем, есть ли уже скрипт
    if "form-ajax.js" in content:
        continue
        
    # Вставляем перед </body>
    if "</body>" in content:
        new_content = content.replace("</body>", f"{script_tag}\n</body>")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Injected AJAX script into {file_path}")
