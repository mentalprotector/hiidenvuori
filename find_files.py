
import os

target_dir = 'assets/img'
prefixes = ['tr7', 'gqd']

for filename in os.listdir(target_dir):
    for prefix in prefixes:
        if filename.startswith(prefix):
            print(filename)
