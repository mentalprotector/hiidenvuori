import os

# Files to process
html_files = [f for f in os.listdir(".") if f.endswith(".html")]

OLD_LOGO_PATH = "assets/img/hm6yw5yu1yoss8ws0c44o44oc4wocs"
NEW_LOGO_PATH = "assets/img/logo.svg"

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if OLD_LOGO_PATH in content:
        print(f"Fixing logo in {file_path}")
        new_content = content.replace(OLD_LOGO_PATH, NEW_LOGO_PATH)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

print("Logo paths updated.")
