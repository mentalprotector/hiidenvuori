import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace carousel background and ship image with high quality local files
# Background
content = re.sub(r"//i\.siteapi\.org/[^\"'\s]*/k8apcr5oe0gsc4c0408wo08g04s8k8", "assets/img/naves.webp", content)
# Ship (using boat_launch as it is the high quality ship photo)
content = re.sub(r"//i\.siteapi\.org/[^\"'\s]*/d6znyknzkmgow48w8coowswgo0w88s", "assets/img/boat_launch.webp", content)

# 2. Localise all other siteapi links
pattern = re.compile(r"//i\.siteapi\.org/[^\"'\s]*/([a-z0-9]{20,})")
content = pattern.sub(r"assets/img/\1.webp", content)

# 3. Clean up phones
content = content.replace("79114057329", "79210146447")
content = content.replace("79212205533", "79210141190")
content = content.replace("+7 (911) 405-73-29", "+7 (921) 014-64-47")
content = content.replace("+7 (921) 220-55-33", "+7 (921) 014-11-90")

# 4. Domain
content = content.replace("https://xn--b1addkdc4ajs2ap.xn--p1ai", "")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
