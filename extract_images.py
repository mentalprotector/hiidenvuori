
import zipfile
import os

zip_path = 'hiidenvuori_backup.zip'
files_to_extract = [
    'assets/img/tr7v205v4s0sogokc0g0wo04g8wgwk.webp',
    'assets/img/gqdsqerf5ao80wgskgk0gggc08k00w.webp'
]

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for file_name in files_to_extract:
        try:
            zip_ref.extract(file_name, '.')
            print(f"Extracted: {file_name}")
        except KeyError:
            print(f"File not found in zip: {file_name}")
            
            # Try to find it loosely
            for zip_info in zip_ref.infolist():
                if os.path.basename(file_name) in zip_info.filename:
                    print(f"Found match: {zip_info.filename}")
                    zip_ref.extract(zip_info, '.')
                    print(f"Extracted: {zip_info.filename}")
