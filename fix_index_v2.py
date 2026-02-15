import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix Service Card (Кемпинг)
# It should use Palatka1.webp
# Pattern: find the block with alt="Кемпинг" and nh-horizontal-cards_round-2
service_card_pattern = re.compile(r"(<img alt=\"Кемпинг\" class=\"nh-horizontal-cards_round-2\"[^>]*src=\")([^\"]+)(\"[^>]*>)", re.DOTALL)
content = service_card_pattern.sub(r"\1assets/img/Palatka1.webp\3", content)

# 2. Fix Gallery
# Card 1 (was mziqpz0) -> assets/img/naves.webp
# My previous script replaced mziqpz0 with naves.png/webp globally.
# Card 2 (was np3wb8) -> assets/img/palatka_large.webp
# My previous script replaced np3wb8 with Palatka1.png/webp globally.

# We need to find the gallery block (nh-cards_round-2)
# and specifically the one that currently has Palatka1.webp and change it to palatka_large.webp
# BUT ONLY if it is a gallery card (nh-cards_round-2)

gallery_card_pattern = re.compile(r"(<li class=\"lazyload nh-cards__item.*?src=\"assets/img/)Palatka1\.webp(\".*?</li>)", re.DOTALL)
content = gallery_card_pattern.sub(r"\1palatka_large.webp\2", content)

# Also ensure all siteapi links are gone just in case
pattern_siteapi = re.compile(r"//i\.siteapi\.org/[^\"'\s]*/([a-z0-9]{20,})")
content = pattern_siteapi.sub(r"assets/img/\1.webp", content)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
