
import zipfile

zip_path = 'hiidenvuori_backup.zip'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for file_name in zip_ref.namelist():
        print(file_name)
