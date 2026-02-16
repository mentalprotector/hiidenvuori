
import zipfile
import os

output_filename = 'hiidenvuori_new.zip'
files_to_include = [
    'Dockerfile',
    'docker-compose.yml',
    'hiidenvuori.caddy'
]

# Add all HTML files
for f in os.listdir('.'):
    if f.endswith('.html'):
        files_to_include.append(f)

# Create the zip file
with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add root files
    for file in files_to_include:
        if os.path.exists(file):
            zipf.write(file)
            print(f"Added {file}")
        else:
            print(f"Warning: {file} not found")

    # Add assets directory
    for root, dirs, files in os.walk('assets'):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path)
            print(f"Added {file_path}")

print(f"Created {output_filename}")
