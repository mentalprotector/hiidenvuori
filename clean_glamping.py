import os
from bs4 import BeautifulSoup
import re

# Files to process
html_files = [f for f in os.listdir(".") if f.endswith(".html")]

def clean_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    modified = False

    # 1. Remove Menu Items containing "Глэмпинг"
    # Searching for <a> tags in menu/topbar
    for a in soup.find_all("a"):
        if a.string and "Глэмпинг" in a.string:
            # Check if it's a menu item (usually has parents like li or specific classes)
            # Nethouse menu items: often just <a> in a container or list
            # We will remove the parent if it looks like a list item wrapper, or just the link.
            # Looking at structure, topbar links are direct children often or in simple wrappers.
            
            # Remove the element
            a.decompose()
            modified = True
    
    # 2. Remove Content Blocks with "Глэмпинг" header
    # Searching for H-tags or specific classes containing the text
    for header in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "strong", "b"]):
        if header.string and "Глэмпинг" in header.string:
            # Find the containing block to remove. This is tricky.
            # We verify if it's a section title.
            # Strategy: Go up to the nearest 'column' or 'section' container and remove it?
            # Or just remove the header and subsequent paragraph?
            
            # Specific case for "razmeshhenie.html" - whole block in features list
            feature_item = header.find_parent(class_="nh-features__item")
            if feature_item:
                feature_item.decompose()
                modified = True
                continue

            # Try to be smart: if it's a card title, remove the card.
            card = header.find_parent(class_="cards__item") # Example class, need to verify
            if card:
                card.decompose()
                modified = True
                continue
                
            # If it is inside a text editor block, remove the paragraph or the header
            header.decompose()
            modified = True

    # 3. Remove text occurrences in paragraphs (naive)
    # Be careful not to break HTML structure.
    for text_node in soup.find_all(string=re.compile("Глэмпинг|глэмпинг")):
        if text_node.parent.name in ['script', 'style']: continue
        
        # If it's just a word in a sentence, replacing it might leave weird grammar.
        # "Палатки, автокемпинг, глэмпинг, всё для..." -> "Палатки, автокемпинг, , всё для..."
        new_text = str(text_node).replace(", глэмпинг", "").replace(" глэмпинг,", "").replace("глэмпинг", "")
        text_node.replace_with(new_text)
        modified = True

    # 4. Remove FAQ item "Чем отличается глэмпинг..."
    # Usually <details> or specific accordion structure.
    # Looking at search result: <summary>...Чем отличается глэмпинг...</summary>
    for summary in soup.find_all("summary"):
        if "глэмпинг" in summary.get_text().lower():
            details = summary.find_parent("details")
            if details:
                details.decompose()
                modified = True
    
    # 5. Remove specific review in comment.html
    # "Глэмпинг уютный..."
    # Find blockquote or review container containing this text
    for review in soup.find_all(string=re.compile("Глэмпинг уютный")):
        container = review.find_parent(class_="comment-item") # Hypothetical class
        if not container:
            container = review.find_parent("li") # Often reviews are lists
        if container:
            container.decompose()
            modified = True
        else:
            # Fallback: remove parent paragraph
            p = review.find_parent("p")
            if p: p.decompose()
            modified = True

    if modified:
        print(f"Cleaned {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))

for f in html_files:
    clean_html(f)

print("Cleanup done.")
