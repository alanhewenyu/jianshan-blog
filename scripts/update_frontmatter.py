#!/usr/bin/env python3
"""
Batch update front matter for PaperMod -> Stack theme migration.
- ShowToc: true -> toc: true
- Remove: TocOpen, ShowReadingTime, ShowWordCount, hidemeta
"""

import os
import re
import glob

def update_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has front matter
    if not content.startswith('---'):
        return False

    # Split front matter from body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    fm = parts[1]
    body = parts[2]
    original_fm = fm

    # Replace ShowToc: true with toc: true
    fm = re.sub(r'\nShowToc:\s*true\s*\n', '\ntoc: true\n', fm)
    # Replace ShowToc: false with toc: false
    fm = re.sub(r'\nShowToc:\s*false\s*\n', '\ntoc: false\n', fm)

    # Remove PaperMod-specific fields
    fm = re.sub(r'\nTocOpen:\s*\w+\s*\n', '\n', fm)
    fm = re.sub(r'\nShowReadingTime:\s*\w+\s*\n', '\n', fm)
    fm = re.sub(r'\nShowWordCount:\s*\w+\s*\n', '\n', fm)
    fm = re.sub(r'\nhidemeta:\s*\w+\s*\n', '\n', fm)

    if fm != original_fm:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---' + fm + '---' + body)
        return True
    return False

# Process all posts
count = 0
for lang_dir in ['content/zh/posts', 'content/en/posts']:
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), lang_dir)
    for root, dirs, files in os.walk(base):
        for fname in files:
            if fname == 'index.md':
                fpath = os.path.join(root, fname)
                if update_frontmatter(fpath):
                    count += 1
                    print(f"Updated: {os.path.relpath(fpath, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}")

print(f"\nTotal files updated: {count}")
