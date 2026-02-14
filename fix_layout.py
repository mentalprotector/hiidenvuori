import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

# Regex to find the injected messenger div
messengers_injection_re = re.compile(r'\s*<div class="nh-topbar-contacts" style="display: inline-flex; margin-left: 10px; gap: 5px; vertical-align: middle;">.*?</div>', re.DOTALL)

for file_name in files:
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Clean up messy injections
        new_content = messengers_injection_re.sub('', content)
        
        # 2. Fix header column - instead of empty div, let's make it display:none
        # This prevents it from taking space in the grid if height/padding is defined in CSS
        col_pattern = re.compile(r'(<div class="nh-topbar__column[^>]*horizontal-align-right[^>]*>)\s*</div>', re.DOTALL)
        
        def hide_column(match):
            tag = match.group(1)
            if 'display: none' not in tag:
                tag = tag.replace('style="', 'style="display: none; ')
            return tag + "</div>"
            
        new_content = col_pattern.sub(hide_column, new_content)
        
        if new_content != content:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned up {file_name}")
    except Exception as e:
        print(f"Error {file_name}: {e}")
