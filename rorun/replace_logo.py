import os
import re

html_dir = r'C:\rorun\rorun\html'
logo_path = '../assets/logo.png'

# Regex to match src="..." containing either data:image/png;base64 or aida/ADBb...
pattern = re.compile(r'src="([^"]*(?:data:image/png;base64|aida/ADBb)[^"]*)"')

for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(html_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = pattern.sub(f'src="{logo_path}"', content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {filename}')
