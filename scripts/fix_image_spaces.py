#!/usr/bin/env python3
"""Fix image filenames with spaces in Hugo page bundles."""

import os
import re
from pathlib import Path

POSTS_DIR = Path("/Users/Alan/.claude/worktrees/distracted-buck/jianshan-blog/content/zh/posts")


def fix_bundle(bundle_dir):
    """Fix image filenames and markdown references in a page bundle."""
    index_file = bundle_dir / "index.md"
    if not index_file.exists():
        return 0

    # Find all files with spaces in their names
    renames = {}
    for f in bundle_dir.iterdir():
        if f.is_file() and f.name != "index.md" and ' ' in f.name:
            new_name = f.name.replace(' ', '-')
            renames[f.name] = new_name

    if not renames:
        return 0

    # Rename files
    for old_name, new_name in renames.items():
        old_path = bundle_dir / old_name
        new_path = bundle_dir / new_name
        old_path.rename(new_path)

    # Update markdown references
    content = index_file.read_text(encoding='utf-8')
    for old_name, new_name in renames.items():
        content = content.replace(f']({old_name})', f']({new_name})')
    index_file.write_text(content, encoding='utf-8')

    return len(renames)


def main():
    total = 0
    for bundle in POSTS_DIR.iterdir():
        if bundle.is_dir():
            count = fix_bundle(bundle)
            if count > 0:
                print(f"  Fixed {count} images in: {bundle.name}")
                total += count

    print(f"\nTotal: {total} image files renamed.")


if __name__ == '__main__':
    main()
