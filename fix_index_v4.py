import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace hashes in src with friendly names in the gallery block
content = content.replace('src="assets/img/mziqpz0enhwc8kkg0s8c088wkoswg0"', 'src="assets/img/naves.webp"')
content = content.replace('src="assets/img/np3wb8n21r4kwg4kc4kkoso4ggg880"', 'src="assets/img/palatka_large.webp"')

# Also handle cases where they were already .webp but with hash name
content = content.replace('src="assets/img/mziqpz0enhwc8kkg0s8c088wkoswg0.webp"', 'src="assets/img/naves.webp"')
content = content.replace('src="assets/img/np3wb8n21r4kwg4kc4kkoso4ggg880.webp"', 'src="assets/img/palatka_large.webp"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
