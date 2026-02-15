import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix Service Card (Кемпинг) -> Should be Palatka1.webp
# Find <img alt="Кемпинг" ... src="..." ... /> or similar
pattern_service = re.compile(r'(<img alt="Кемпинг"[^>]+src=")([^"]+)(")', re.DOTALL)
content = pattern_service.sub(r'\1assets/img/Palatka1.webp\3', content)

# 2. Fix Gallery Cards (nh-cards_round-2)
# We want to replace the image in the gallery block.
# Let s find the gallery items.
# Card 1 (was mziqpz0) -> naves.webp
# Card 2 (was np3wb8) -> palatka_large.webp

# I will do a very specific replacement for the gallery block
gallery_items_pattern = re.compile(r'(<ul class="nh-cards__items nh-cards_l nh-cards__items_0 nh-cards__items--adaptive">.*?</ul>)', re.DOTALL)
gallery_match = gallery_items_pattern.search(content)
if gallery_match:
    gallery_block = gallery_match.group(1)
    # Inside this block, replace images
    # Replace any webp that was mziqpz0 (if it still exists or was already localized)
    gallery_block = re.sub(r'assets/img/mziqpz0[^\"]*\.webp', 'assets/img/naves.webp', gallery_block)
    # Replace any webp that was np3wb8
    gallery_block = re.sub(r'assets/img/np3wb8[^\"]*\.webp', 'assets/img/palatka_large.webp', gallery_block)
    
    # Update the content
    content = content.replace(gallery_match.group(1), gallery_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
