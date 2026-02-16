
import os

files_to_fix = [
    'razmeshhenie.html',
    'aktivnyj-otdykh.html',
    'comment.html',
    'uslugi.html', # I fixed this one via replace earlier, but let's double check
    'contacts.html' # Fixed via replace earlier
]

# The item we want to ensure exists after the first phone number
new_phone_item = """<li class="nh-burger-menu__links-item">
<a class="nh-burger-menu__link" href="tel:+79210146447" style="--item-color: #FFFFFF; --item-hover: #3384BF;" target="_parent">
                                            +7 (921) 014-64-47
                                        </a>
</li>"""

search_str = 'class="nh-burger-menu__link" href="tel:+79210141190"'

for filename in files_to_fix:
    if not os.path.exists(filename):
        continue

    print(f"Processing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Isolate the burger menu section
    burger_menu_start = content.find('class="nh-burger-menu')
    if burger_menu_start == -1:
        print(f"  Burger menu not found in {filename}")
        continue
        
    burger_menu_end = content.find('</section>', burger_menu_start)
    if burger_menu_end == -1:
        print(f"  Burger menu end not found in {filename}")
        continue

    burger_content = content[burger_menu_start:burger_menu_end]
    
    # Find the first phone number
    first_idx = burger_content.find(search_str)
    
    if first_idx != -1:
        # Find the end of this list item
        # The structure is: 
        # <li ...>
        #   <a ...> ... </a>
        # </li>
        
        # We found the <a> tag start. We need to find the closing </li> AFTER the </a>
        link_end = burger_content.find('</a>', first_idx)
        li_end = burger_content.find('</li>', link_end)
        
        if li_end != -1:
            insertion_point = li_end + 5 # after </li>
            
            # Check what's next
            next_content = burger_content[insertion_point:].strip()
            
            # If the next thing is another phone link (duplicate or not), we handle it
            if 'href="tel:+79210141190"' in next_content[:200]:
                print(f"  Found duplicate phone (via peek). Replacing...")
                # It's a duplicate of the first one. We need to replace it.
                # Find the extent of this second duplicate
                dup_start = burger_content.find('<li', insertion_point)
                dup_link = burger_content.find(search_str, insertion_point)
                dup_end = burger_content.find('</li>', dup_link) + 5
                
                # Replace the duplicate block with the new item
                new_burger_content = burger_content[:dup_start] + "\n" + new_phone_item + burger_content[dup_end:]
                
                new_full_content = content[:burger_menu_start] + new_burger_content + content[burger_menu_end:]
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_full_content)
                print(f"  Fixed duplicate in {filename}")
                
            elif 'href="tel:+79210146447"' in next_content[:200]:
                print(f"  Second phone already exists in {filename}")
            else:
                print(f"  Second phone missing. Adding it...")
                # Add the new item
                new_burger_content = burger_content[:insertion_point] + "\n" + new_phone_item + burger_content[insertion_point:]
                
                new_full_content = content[:burger_menu_start] + new_burger_content + content[burger_menu_end:]
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_full_content)
                print(f"  Added missing phone to {filename}")
        else:
            print("  Could not find closing </li>")
            
    else:
        print(f"  No phone link found in burger menu of {filename}")
