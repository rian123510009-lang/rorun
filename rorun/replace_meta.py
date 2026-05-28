import os
import re

html_dir = r'C:\rorun\rorun\html'
pattern = re.compile(r'<meta content="width=device-width, initial-scale=1.0" name="viewport">')
replacement = '<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport">'

for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(html_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = pattern.sub(replacement, content)
        
        # also check for alternative meta tag orders
        alt_pattern = re.compile(r'<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        new_content = alt_pattern.sub(replacement, new_content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {filename}')
