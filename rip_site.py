import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

# Config
BASE_URL = "https://hiidenvuori.nethouse.ru"
ASSETS_DIR = "assets"
# We will track visited pages to avoid loops
visited_pages = set()
pages_to_visit = ["/"] # Start with root

# Create directories
for subdir in ["css", "js", "img", "fonts"]:
    os.makedirs(os.path.join(ASSETS_DIR, subdir), exist_ok=True)

def download_asset(url, type_folder):
    if not url: return url
    original_url = url
    
    if url.startswith("//"):
        url = "https:" + url
    
    if not url.startswith("http"):
        if url.startswith("/"):
            url = BASE_URL + url
        else:
            url = BASE_URL + "/" + url

    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename: return original_url
    
    if "%" in filename: 
        filename = urllib.parse.unquote(filename)
    
    local_path = os.path.join(ASSETS_DIR, type_folder, filename)
    
    try:
        if not os.path.exists(local_path):
            print(f"   -> Downloading asset {filename}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        return f"{ASSETS_DIR}/{type_folder}/{filename}"
    except Exception as e:
        # print(f"Failed asset: {url}")
        return original_url

def process_page(page_path):
    if page_path in visited_pages:
        return
    visited_pages.add(page_path)
    
    # Determine local filename
    if page_path == "/" or page_path == "":
        local_filename = "index.html"
    else:
        # e.g. /contacts -> contacts.html
        local_filename = page_path.strip("/") + ".html"
    
    print(f"Processing Page: {page_path} -> {local_filename}")
    
    full_url = BASE_URL + page_path
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
    except Exception as e:
        print(f"Failed to fetch page {full_url}: {e}")
        return

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Find other internal pages to crawl
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Logic to find internal pages: starts with / and no extension (usually)
        if href.startswith("/") and not href.startswith("//"):
            if "." not in href.split("/")[-1]: # simplistic check for "not a file"
                if href not in visited_pages:
                    pages_to_visit.append(href)
            
            # Rewrite link to .html for local navigation
            if href == "/":
                a["href"] = "index.html"
            else:
                clean_href = href.strip("/")
                a["href"] = clean_href + ".html"

    # 2. Localize Assets
    
    # CSS
    for link in soup.find_all("link", rel="stylesheet"):
        if link.get("href"):
            # Fix relative paths in CSS imports if needed? Nethouse usually absolute.
            link["href"] = download_asset(link["href"], "css")
            # If we are in a sub-page (e.g. contacts.html), assets are in assets/..
            # But wait, we are saving all htmls in root. So assets/ is correct.

    # JS
    for script in soup.find_all("script", src=True):
        if script.get("src"):
            script["src"] = download_asset(script["src"], "js")

    # Images
    for img in soup.find_all("img", src=True):
        if img.get("src"):
            img["src"] = download_asset(img["src"], "img")
            if img.get("srcset"): del img["srcset"]

    # Favicons
    for link in soup.find_all("link", rel=lambda x: x and "icon" in x):
        if link.get("href"):
            link["href"] = download_asset(link["href"], "img")

    # Backgrounds
    url_pattern = re.compile(r'url\((.*?)\)')
    def replace_url(match):
        raw_url = match.group(1).strip('\'"')
        new_url = download_asset(raw_url, 'img')
        return f"url('{new_url}')"

    for tag in soup.find_all(style=True):
        if "url(" in tag["style"]:
            tag["style"] = url_pattern.sub(replace_url, tag["style"])

    # Save
    with open(local_filename, "w", encoding="utf-8") as f:
        f.write(str(soup))


# Main Loop
while len(pages_to_visit) > 0:
    next_page = pages_to_visit.pop(0)
    process_page(next_page)

print("Crawling complete!")
