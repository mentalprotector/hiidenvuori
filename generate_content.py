import re

try:
    with open('stoyanka-dlya-avtodomov.html', 'r', encoding='utf-8') as f:
        content = f.read()

    def extract_section(html, section_id):
        pattern = r'(<section[^>]*id="' + section_id + r'"[^>]*>.*?</section>)'
        match = re.search(pattern, html, re.DOTALL)
        return match.group(1) if match else None

    cards_65 = extract_section(content, 'cards-65')
    cards_66 = extract_section(content, 'cards-66')

    final_price_section = ""
    final_free_section = ""

    # Process cards-65 (Price List)
    if cards_65:
        # Change Title
        # Note: checking for exact string match might fail if there are hidden chars or slightly different whitespace in the file vs what I read
        # I'll use regex for the title replacement to be safer
        
        cards_65_new = cards_65.replace('id="cards-65"', 'id="cards-razmeshhenie-price"')
        cards_65_new = re.sub(r'Прейскурант на услуги\s*<br/>\s*автокемпинга «Хийденвуори»', 'Прейскурант на услуги <br/> кемпинга «Хийденвуори»', cards_65_new)
        
        # Extract LIs
        lis = re.findall(r'(<li.*?</li>)', cards_65_new, re.DOTALL)
        
        selected_lis = []
        # 1. Tent place (1500)
        for li in lis:
            if 'Место <br/>для палатки' in li and '1500,00' in li:
                selected_lis.append(li)
                break
        # 2. Tent under canopy (2000)
        for li in lis:
            if 'Место для палатки <br/>под навесом' in li and '2000,00' in li:
                selected_lis.append(li)
                break
        # 3. Tent natural ground (700)
        for li in lis:
            if 'Место для палатки <br/>на естественном грунте' in li and '700,00' in li:
                selected_lis.append(li)
                break
        # 4. Shower (350)
        for li in lis:
            if 'Душ<br/>' in li and '350 руб.' in li:
                selected_lis.append(li)
                break
                
        # Reconstruct the list
        # Find the ul
        ul_start = cards_65_new.find('<ul')
        if ul_start != -1:
            ul_content_start = cards_65_new.find('>', ul_start) + 1
            ul_end = cards_65_new.find('</ul>')
            
            new_ul_content = '\n'.join(selected_lis)
            
            final_price_section = cards_65_new[:ul_content_start] + new_ul_content + cards_65_new[ul_end:]
        else:
             print("Could not find UL in cards-65")

    # Process cards-66 (Free)
    if cards_66:
        final_free_section = cards_66.replace('id="cards-66"', 'id="cards-razmeshhenie-free"')

    with open('new_content.html', 'w', encoding='utf-8') as f:
        f.write(final_price_section + '\n' + final_free_section)
    
    print("Content generated successfully.")

except Exception as e:
    print(f"Error: {e}")
