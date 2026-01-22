import os
import re

# Files to process
html_files = [f for f in os.listdir(".") if f.endswith(".html")]

def remove_informer(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pattern to match the Yandex.Metrika informer block
    # It usually starts with <!-- Yandex.Metrika informer --> and ends with <!-- /Yandex.Metrika informer -->
    pattern = r'<!-- Yandex\.Metrika informer -->.*?<!-- /Yandex\.Metrika informer -->'
    
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Removed informer from {file_path}")

for f in html_files:
    remove_informer(f)

print("Yandex Informer cleanup complete.")
