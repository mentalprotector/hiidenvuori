import os
import re

# CSS Patch for Nethouse legacy code to fix mobile view
MOBILE_CSS_PATCH = """
<style>
    /* EMERGENCY RESPONSIVE PATCH */
    @media screen and (max-width: 1024px) {
        body, html { overflow-x: hidden !important; width: 100% !important; }
        
        /* Make images responsive */
        img, video, iframe, svg { 
            max-width: 100% !important; 
            height: auto !important; 
        }
        
        /* Reset fixed widths on containers */
        .container, .row, .column, [class*="grid"], [style*="width"] {
            width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }
        
        /* Fix padding on mobile */
        .container { padding-left: 15px !important; padding-right: 15px !important; }
        
        /* Menu fixes */
        .nh-topbar__column { width: 100% !important; display: block !important; text-align: center !important; }
        .nh-topbar-link { display: inline-block !important; padding: 10px !important; }
    }
</style>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""

def clean_title(title_text):
    # If title is mojibake (detect via common weird chars), replace it
    if "╨" in title_text or "╥" in title_text:
        return "Хийденвуори | Туристическое пространство в Карелии"
    return title_text

def patch_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    
    # 1. Fix Mojibake in Title
    # Extract title
    match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if match:
        old_title = match.group(1)
        new_title = clean_title(old_title)
        if new_title != old_title:
            content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')

    # 2. Inject CSS Patch
    # Insert before </head>
    if "</head>" in content and "EMERGENCY RESPONSIVE PATCH" not in content:
        content = content.replace("</head>", MOBILE_CSS_PATCH + "\n</head>")

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Patched {file_path}")

html_files = [f for f in os.listdir(".") if f.endswith(".html")]

for f in html_files:
    patch_file(f)

print("All files patched.")
