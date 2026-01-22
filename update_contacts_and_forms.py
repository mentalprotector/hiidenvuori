import os
import re
from bs4 import BeautifulSoup

# Config
NEW_EMAIL = "mail@hiidenvuori.ru"
OLD_PHONE_WHATSAPP = "79114057329"
NEW_PHONE_WHATSAPP = "+79114057329" # With plus
COORDS = "61.708259, 30.981770"

# Formspree Endpoint (User needs to claim this form)
# When they submit the first time, Formspree will ask them to verify email.
FORMSPREE_ACTION = "https://formspree.io/f/mrgvnqzw" # Generic placeholder, user should update or claim

def patch_contacts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False

    # 1. Replace Email (in text and mailto links)
    # Search for old email text patterns or just replace any mailto link that isn't the new one
    # Assuming old email might be info@hiidenvuori.ru or nethouse one
    # Let's find all mailto links
    for a in soup.find_all("a", href=re.compile(r"^mailto:")):
        if a["href"] != f"mailto:{NEW_EMAIL}":
            a["href"] = f"mailto:{NEW_EMAIL}"
            # Also update text content if it looks like an email
            if "@" in a.get_text():
                a.string = NEW_EMAIL
            modified = True
    
    # 2. Fix WhatsApp Link
    # Searching for links containing the old number
    for a in soup.find_all("a", href=True):
        if OLD_PHONE_WHATSAPP in a["href"] and "+" not in a["href"]:
            a["href"] = a["href"].replace(OLD_PHONE_WHATSAPP, NEW_PHONE_WHATSAPP)
            modified = True

    # 3. Add Coordinates with Copy Button (Specifically for contacts.html)
    if "contacts.html" in file_path:
        # Find the address block to append coordinates
        # Look for "Республика Карелия..." text
        address_div = soup.find("div", string=re.compile("Республика Карелия"))
        if address_div:
            # Check if already added
            if "61.708259" not in str(address_div.parent):
                coords_html = BeautifulSoup(f"""
                <div class="contact-address__part" style="margin-top: 10px;">
                    <span id="coords-text">{COORDS}</span>
                    <button onclick="navigator.clipboard.writeText('{COORDS}'); alert('Координаты скопированы!');" style="
                        background: none; 
                        border: 1px solid #3384BF; 
                        color: #3384BF; 
                        padding: 2px 8px; 
                        border-radius: 4px; 
                        cursor: pointer; 
                        margin-left: 10px;
                        font-size: 12px;">Копировать</button>
                </div>
                """, "html.parser")
                address_div.parent.append(coords_html)
                modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Updated contacts info in {file_path}")

def patch_forms(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False
    
    # Find forms that look like lead/contact forms
    # Nethouse forms usually have class "nh-application-form-container" or similar
    forms = soup.find_all("form")
    for form in forms:
        # Check if it's a real form (has inputs)
        if form.find("input"):
            # Change action to Formspree
            form["action"] = FORMSPREE_ACTION
            form["method"] = "POST"
            
            # Remove Nethouse specific JS handlers to prevent interference
            # Usually they bind via ID or Class. We can add a 'onsubmit' attribute to stop propagation if needed,
            # but usually changing 'action' is enough if we remove the Nethouse script.
            # But we can't remove main script easily.
            # We will add a small inline script to stop event bubbling? 
            # Better: remove the 'id' that Nethouse JS attaches to?
            # Nethouse uses ID like 'application-form-action-31'
            # Let's change the ID slightly so Nethouse JS doesn't recognize it
            if form.get("id"):
                form["id"] = form["id"] + "_static" 
            
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Updated forms in {file_path}")

# Run
html_files = [f for f in os.listdir("hiidenvuori") if f.endswith(".html")]
for f in html_files:
    full_path = os.path.join("hiidenvuori", f)
    patch_contacts(full_path)
    patch_forms(full_path)
