import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. FIX PHONES (to main number)
content = content.replace("79114057329", "79210141190")
content = content.replace("79212205533", "79210141190")
content = content.replace("+7 (911) 405-73-29", "+7 (921) 014-11-90")
content = content.replace("+7 (921) 220-55-33", "+7 (921) 014-11-90")

# 2. FIX DOMAIN (relative paths)
content = content.replace("https://xn--b1addkdc4ajs2ap.xn--p1ai/", "/")
content = content.replace("https://xn--b1addkdc4ajs2ap.xn--p1ai", "")

# 3. LOCALISE ALL SITEAPI LINKS
# Replace //i.siteapi.org/.../HASH with assets/img/HASH.webp
pattern_siteapi = re.compile(r"//i\.siteapi\.org/[^\"'\s]*/([a-z0-9]{20,})")
content = pattern_siteapi.sub(r"assets/img/\1.webp", content)

# 4. FIX CONCERT CARD -> BOAT LAUNCH (Keeping the original layout)
# Hash for concert image was 7ilwtoolxu8sskw08ccg80kw0ckkww
content = content.replace("assets/img/7ilwtoolxu8sskw08ccg80kw0ckkww.webp", "assets/img/boat_launch.webp")
content = content.replace("Концертные программы", "Спуск для катеров")
old_desc = "Органные концерты проходят в на берегу Ладоги в Хийденвуори ив старинной Сортавале"
new_desc = "На территории имеется оборудованный спуск на воду для катеров, что делает отдых ещё более удобным для владельцев водного транспорта."
content = content.replace(old_desc, new_desc)

# 5. RESTORE PAIRED PHONES IN MAP BLOCK
content = content.replace("+7 (921) 014-11-90<br/>+7 (921) 014-11-90", "+7 (921) 014-11-90<br/>+7 (921) 014-64-47")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
