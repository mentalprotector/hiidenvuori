
import os

target = 'konczertnye-programmy.html'
replacement = 'spusk-dlya-katerov.html'

files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if target in content:
        print(f"Fixing {filename}...")
        new_content = content.replace(target, replacement)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        print(f"Clean: {filename}")
