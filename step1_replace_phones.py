import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

repls = [
    (r'\+79210141190', '+79210149011'),
    (r'\+79114057329', '+79210146447'),
    (r'79210141190', '79210149011'),
    (r'79114057329', '79210146447'),
    (r'\+7 \(921\) 014-11-90', '+7 (921) 014-90-11'),
    (r'\+7 \(911\) 405-73-29', '+7 (921) 014-64-47'),
    (r'\+79212205533', '+79210149011'),
]

for file_name in files:
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for pattern, repl in repls:
        new_content = re.sub(pattern, repl, new_content)
    
    if new_content != content:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated phones in {file_name}")
