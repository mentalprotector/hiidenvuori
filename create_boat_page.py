
import os

with open('transfer-v-ruskealu.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace specific content
content = content.replace('<title>Хийденвуори.рф | Туристическое пространство на Ладожском озере! - Трансфер в Рускеалу</title>', '<title>Хийденвуори.рф | Туристическое пространство на Ладожском озере! - Спуск для катеров</title>')
content = content.replace('<link href="/transfer-v-ruskealu" rel="canonical"/>', '<link href="/spusk-dlya-katerov" rel="canonical"/>')
content = content.replace('<meta content="Трансфер в Рускеалу" property="og:title"/>', '<meta content="Спуск для катеров" property="og:title"/>')
content = content.replace('<meta content="https://хийденвуори.рф/transfer-v-ruskealu" property="og:url"/>', '<meta content="https://хийденвуори.рф/spusk-dlya-katerov" property="og:url"/>')
content = content.replace('<h1>Трансфер в Рускеалу</h1>', '<h1>Спуск для катеров</h1>')

# Replace the main text content
old_text_block = """<div class="nh-features__title nh-features-item-title--user-inner nh-features__title--align-left" style="color: #243B5C;">
<h2 class="nh-text-editor__fontsize-28">Трансфер в горный парк Рускеала</h2> </div>
<div class="nh-features__text nh-features-item-desc--user-inner" style="color: #102748;">
<p class="nh-text-editor__fontsize-16"><strong>Желаете отправиться в незабываемое путешествие и прикоснуться к великолепию северной природы? </strong></p><p class="nh-text-editor__fontsize-16">Горный парк Рускеала приглашает вас окунуться в мир уникальной природы Карелии и вдохнуть атмосферу древней истории и традиций!</p><p class="nh-text-editor__fontsize-16">Горный парк Рускеала — это уникальный природный и культурно-исторический объект, расположенный в Карелии, на северо-западе России. Известный своими живописными мраморными каньонами, подземными галереями и исторической добычей мрамора, парк привлекает тысячи туристов со всего мира.</p><h6 class="nh-text-editor__fontsize-16">Почему стоит посетить Рускеалу?</h6><ul><li class="nh-text-editor__fontsize-16">Живописные пейзажи: Голубые воды каньонов, живописные скалы и величие древних карьеров создают атмосферу настоящего восхищения.</li><li class="nh-text-editor__fontsize-16">Историческое наследие: Парк сохраняет память о долгой истории добычи мрамора, знаменитого своим качеством и применявшегося при строительстве петербургских дворцов и храмов.</li><li class="nh-text-editor__fontsize-16">Активный отдых: Здесь можно насладиться прогулками по каньонам, прокатиться на лодках, исследовать подземные галереи и поучаствовать в разнообразных мероприятиях.</li></ul><p class="nh-text-editor__fontsize-16"><strong>Не упустите возможность совершить увлекательное путешествие в уникальный горный парк Рускеала и погрузиться в мир северных чудес Карелии!</strong></p> </div>"""

new_text_block = """<div class="nh-features__title nh-features-item-title--user-inner nh-features__title--align-left" style="color: #243B5C;">
<h2 class="nh-text-editor__fontsize-28">Спуск для катеров</h2> </div>
<div class="nh-features__text nh-features-item-desc--user-inner" style="color: #102748;">
<p class="nh-text-editor__fontsize-16"><strong>На территории имеется оборудованный спуск на воду для катеров, что делает отдых ещё более удобным для владельцев водного транспорта.</strong></p>
<p class="nh-text-editor__fontsize-16">Мы предлагаем удобный подъезд к воде, позволяющий безопасно спустить ваше судно. Вы можете наслаждаться прогулками по Ладожским шхерам на собственном катере или лодке.</p>
<p class="nh-text-editor__fontsize-16">Также доступна аренда места для стоянки прицепа.</p>
<div class="nh-features__btn-container nh-features__btn-container--alignment-0" style="margin-top: 20px;">
<a class="nh-features__btn nh-features__btn--basic nh-features__btn--size-l" href="https://t.me/+79210141190" target="_blank">
                                                                    Узнать стоимость
                                                                </a>
</div>
</div>"""

content = content.replace(old_text_block, new_text_block)

# Replace the image in the features section
# Old image in transfer-v-ruskealu.html: assets/img/c5a6bs66mc0884kg8cwoccs8c88sg0.webp
# New image: assets/img/boat_launch.webp (I saw this file exists)

content = content.replace('c5a6bs66mc0884kg8cwoccs8c88sg0.webp', 'boat_launch.webp')
# Replace variations (png, etc if they exist in text, but likely the regex replacement handles webp)
# Actually, the file has srcset with hashes. I should replace all occurrences of that hash.
content = content.replace('c5a6bs66mc0884kg8cwoccs8c88sg0', 'boat_launch') 
# Note: 'boat_launch.webp' is the filename. The hash replacement might break extension if not careful.
# In the html: src="assets/img/c5a6bs66mc0884kg8cwoccs8c88sg0.webp"
# Replacement: src="assets/img/boat_launch.webp"

with open('spusk-dlya-katerov.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created spusk-dlya-katerov.html")
