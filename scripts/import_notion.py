#!/usr/bin/env python3
"""
Import Notion exported articles into Hugo blog.
Reads CSV for metadata, converts markdown, copies images using page bundles.
"""

import csv
import os
import re
import shutil
import unicodedata
from pathlib import Path
from urllib.parse import unquote

# Paths
EXPORT_DIR = Path("/Users/Alan/ExportBlock-bd5f065a-45a8-4f61-bc26-6638c34093df-Part-1/见山笔记")
CSV_FILE = Path("/Users/Alan/ExportBlock-bd5f065a-45a8-4f61-bc26-6638c34093df-Part-1/见山笔记 209f81bd42134afa8cb5402ee94b5680_all.csv")
HUGO_CONTENT_DIR = Path("/Users/Alan/.claude/worktrees/distracted-buck/jianshan-blog/content/zh/posts")


def slugify(title):
    """Generate a URL-friendly slug from a Chinese/English title."""
    # Remove special chars, keep Chinese, alphanumeric, spaces, hyphens
    slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = slug.lower()
    return slug


def find_md_file(title):
    """Find the markdown file for a given title in the export directory."""
    for f in EXPORT_DIR.iterdir():
        if f.suffix == '.md' and f.name.startswith(title[:20]):
            return f
    # Try more fuzzy matching
    title_clean = title.replace('\n', '').strip()
    for f in EXPORT_DIR.iterdir():
        if f.suffix == '.md':
            # Extract title from filename (before the hash)
            fname = f.stem
            # Remove the trailing hash (32 hex chars)
            fname_title = re.sub(r'\s+[0-9a-f]{32}$', '', fname)
            if fname_title == title_clean:
                return f
    return None


def find_image_dir(title):
    """Find the image directory for a given article."""
    title_clean = title.replace('\n', '').strip()
    for d in EXPORT_DIR.iterdir():
        if d.is_dir() and d.name.startswith(title_clean[:30]):
            return d
    # Try exact match
    for d in EXPORT_DIR.iterdir():
        if d.is_dir() and d.name == title_clean:
            return d
    return None


def process_markdown(content, image_dir_name):
    """
    Process Notion markdown:
    1. Remove the Notion metadata header (title, type, status, date, category)
    2. Fix image paths to use page bundle relative paths
    """
    lines = content.split('\n')

    # Remove the title (first H1) and metadata lines
    body_start = 0
    if lines and lines[0].startswith('# '):
        body_start = 1

    # Skip metadata lines (type:, status:, date:, category:, summary:, slug:, icon:, password:)
    metadata_keys = ['type:', 'status:', 'date:', 'category:', 'summary:', 'slug:', 'icon:', 'password:']
    while body_start < len(lines):
        line = lines[body_start].strip()
        if line == '':
            body_start += 1
            continue
        if any(line.lower().startswith(k) for k in metadata_keys):
            body_start += 1
            continue
        break

    body = '\n'.join(lines[body_start:])

    # Fix image paths: ![alt](encoded_dir_name/image.png) -> ![alt](image.png)
    def fix_image_path(match):
        alt = match.group(1)
        path = unquote(match.group(2))
        # Extract just the filename from the path
        filename = os.path.basename(path)
        return f'![{alt}]({filename})'

    body = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_path, body)

    return body.strip()


def generate_tags(title, category, content):
    """Generate relevant tags based on content keywords."""
    tag_keywords = {
        'DCF': ['DCF', '现金流折现', '折现'],
        '价值投资': ['价值投资', '内在价值', '安全边际'],
        'ROIC': ['ROIC', '资本回报率'],
        '巴菲特': ['巴菲特', 'Buffett', '伯克希尔'],
        '芒格': ['芒格', 'Munger'],
        '财务报表': ['财务报表', '财报', '利润表', '现金流量表', '资产负债表'],
        '估值': ['估值', 'valuation'],
        '指数基金': ['指数基金', 'ETF', 'Vanguard'],
        'WACC': ['WACC', '加权平均资本成本'],
        '茅台': ['茅台'],
        '腾讯': ['腾讯'],
        '阿里巴巴': ['阿里巴巴', '阿里'],
        '美团': ['美团'],
        '拼多多': ['拼多多', '黄峥'],
        '香港': ['香港', '港股'],
        'A股': ['A股'],
        'B股': ['B股'],
        '人民币': ['人民币', '汇率'],
        'AI': ['AI', 'GPT', '人工智能'],
        'IFRS': ['IFRS', '会计准则'],
        '普华永道': ['普华永道', 'PwC'],
        '恒大': ['恒大'],
        '市盈率': ['市盈率', 'P/E', 'PE'],
        '消费': ['消费行业', '消费'],
        '税收': ['税收', '财税'],
    }

    tags = []
    full_text = title + ' ' + content
    for tag, keywords in tag_keywords.items():
        for kw in keywords:
            if kw in full_text:
                tags.append(tag)
                break
    return tags


def main():
    # Read CSV to get published articles
    articles = []
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('title', '').strip()
            status = row.get('status', '').strip()
            article_type = row.get('type', '').strip()
            date = row.get('date', '').strip()
            category = row.get('category', '').strip()
            summary = row.get('summary', '').strip()
            slug = row.get('slug', '').strip()

            # Only process Published Posts
            if status == 'Published' and article_type == 'Post' and title and date:
                articles.append({
                    'title': title,
                    'date': date,
                    'category': category,
                    'summary': summary,
                    'slug': slug,
                })

    print(f"Found {len(articles)} published articles to import.\n")

    success_count = 0
    failed = []

    for article in articles:
        title = article['title']
        print(f"Processing: {title}")

        # Find markdown file
        md_file = find_md_file(title)
        if not md_file:
            print(f"  ❌ Markdown file not found!")
            failed.append(title)
            continue

        # Read markdown content
        content = md_file.read_text(encoding='utf-8')

        # Find image directory
        image_dir = find_image_dir(title)
        image_dir_name = image_dir.name if image_dir else ""

        # Process markdown
        body = process_markdown(content, image_dir_name)

        # Generate slug
        slug = article['slug'] if article['slug'] else slugify(title)

        # Generate tags
        tags = generate_tags(title, article['category'], body)

        # Format date
        date = article['date'].replace('/', '-')

        # Build front matter
        categories = f'["{article["category"]}"]' if article['category'] else '[]'
        tags_str = ', '.join(f'"{t}"' for t in tags)

        front_matter = f"""---
title: "{title}"
date: {date}
draft: false
slug: "{slug}"
categories: {categories}
tags: [{tags_str}]
summary: "{article['summary']}"
ShowToc: true
TocOpen: false
---"""

        # Create page bundle directory
        bundle_dir = HUGO_CONTENT_DIR / slug
        bundle_dir.mkdir(parents=True, exist_ok=True)

        # Write index.md
        output_file = bundle_dir / "index.md"
        output_file.write_text(front_matter + '\n\n' + body, encoding='utf-8')

        # Copy images if they exist
        if image_dir and image_dir.is_dir():
            img_count = 0
            for img in image_dir.iterdir():
                if img.is_file():
                    shutil.copy2(img, bundle_dir / img.name)
                    img_count += 1
            print(f"  ✅ Created with {img_count} images")
        else:
            print(f"  ✅ Created (no images)")

        success_count += 1

    print(f"\n{'='*50}")
    print(f"Import complete: {success_count} articles imported successfully.")
    if failed:
        print(f"Failed ({len(failed)}):")
        for t in failed:
            print(f"  - {t}")


if __name__ == '__main__':
    main()
