import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find siteapi links and extract the hash
# Matches //i.siteapi.org/.../HASH
pattern = re.compile(r"//i\.siteapi\.org/[^\"'\s]*/([a-z0-9]{20,})")

# Replace with local path
new_content = pattern.sub(r"assets/img/\1.webp", content)

# Also fix the phones and domain just in case they were reverted
new_content = new_content.replace("79114057329", "79210141190")
new_content = new_content.replace("79212205533", "79210141190")
new_content = new_content.replace("https://xn--b1addkdc4ajs2ap.xn--p1ai", "")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
