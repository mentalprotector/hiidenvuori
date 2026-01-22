import os
import glob

# CSS tag to inject
css_tag = '<link href="assets/css/burger-fix.css" rel="stylesheet" type="text/css"/>'

html_files = glob.glob("hiidenvuori/*.html")

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if already injected
    if "burger-fix.css" in content:
        continue
        
    # Inject before </head>
    if "</head>" in content:
        new_content = content.replace("</head>", f"{css_tag}\n</head>")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Injected burger-fix CSS into {file_path}")
