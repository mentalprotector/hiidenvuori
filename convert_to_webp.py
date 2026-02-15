import os
import subprocess
import re

ffmpeg_path = "/home/matveyrl-1/.local/bin/ffmpeg"
img_dir = "/home/matveyrl-1/hiidenvuori/assets/img"
html_files = [
    "/home/matveyrl-1/hiidenvuori/index.html",
    "/home/matveyrl-1/hiidenvuori/uslugi.html",
    "/home/matveyrl-1/hiidenvuori/razmeshhenie.html",
    "/home/matveyrl-1/hiidenvuori/stoyanka-dlya-avtodomov.html",
    "/home/matveyrl-1/hiidenvuori/contacts.html",
    "/home/matveyrl-1/hiidenvuori/agreement.html",
    "/home/matveyrl-1/hiidenvuori/privacy.html",
    "/home/matveyrl-1/hiidenvuori/aktivnyj-otdykh.html",
    "/home/matveyrl-1/hiidenvuori/comment.html",
    "/home/matveyrl-1/hiidenvuori/magazin-kafe-saha.html",
    "/home/matveyrl-1/hiidenvuori/rules.html",
    "/home/matveyrl-1/hiidenvuori/transfer-v-ruskealu.html"
]

def convert_to_webp(filename):
    base, ext = os.path.splitext(filename)
    if ext.lower() in [".png", ".jpg", ".jpeg"]:
        input_path = os.path.join(img_dir, filename)
        output_path = os.path.join(img_dir, base + ".webp")
        
        # Skip if webp already exists and is newer? No, let's overwrite to be sure.
        cmd = [ffmpeg_path, "-y", "-i", input_path, output_path]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True, filename, base + ".webp"
        except subprocess.CalledProcessError as e:
            print(f"Error converting {filename}: {e}")
            return False, None, None
    return False, None, None

conversions = []
for filename in os.listdir(img_dir):
    success, old, new = convert_to_webp(filename)
    if success:
        conversions.append((old, new))

# Update HTML files
for html_path in html_files:
    if not os.path.exists(html_path):
        continue
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    for old, new in conversions:
        # Replace filename
        content = content.replace(old, new)
        # Also handle cases where only the extension changed but base name was already used
        # (Though our conversion keeps base name)
    
    # Fix any remaining .png or .jpg references that might have been missed 
    # (e.g. if the file was deleted but reference stayed)
    content = re.sub(r"assets/img/([a-zA-Z0-9_-]+)\.(png|jpg|jpeg)", r"assets/img/\1.webp", content)

    if content != original_content:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated references in {html_path}")

# Cleanup old files
for old, new in conversions:
    path = os.path.join(img_dir, old)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {old}")
