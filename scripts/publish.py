#!/usr/bin/env python3
"""
Import a WeChat (微信公众号) article into the Hugo blog.

Usage:
    python scripts/publish.py "https://mp.weixin.qq.com/s/xxxxx" --category "公司估值"
    python scripts/publish.py "https://mp.weixin.qq.com/s/xxxxx" --category "生活感悟" --no-translate
    python scripts/publish.py "https://mp.weixin.qq.com/s/xxxxx" --dry-run

Dependencies:
    pip install -r scripts/requirements.txt
"""

import argparse
import mimetypes
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString
from markdownify import MarkdownConverter

# ==================
# Configuration
# ==================

BLOG_ROOT = Path(__file__).resolve().parent.parent
ZH_POSTS_DIR = BLOG_ROOT / "content" / "zh" / "posts"
EN_POSTS_DIR = BLOG_ROOT / "content" / "en" / "posts"

# Mobile WeChat User-Agent to bypass anti-scraping
WECHAT_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Mobile/15E148 MicroMessenger/8.0.43(0x18002b2d) "
    "NetType/WIFI Language/zh_CN"
)

# Category mapping: Chinese → English
CATEGORY_MAP = {
    "公司估值": "Company Valuation",
    "商业分析": "Business Analysis",
    "生活感悟": "Life Reflections",
    "投资思考": "Investment Thinking",
    "数据分析": "Data Analysis",
    "工具分享": "Tools & Resources",
}

# Tag keyword detection (Chinese keyword → tag name)
TAG_KEYWORDS = {
    "DCF": ["DCF", "现金流折现", "折现"],
    "价值投资": ["价值投资", "内在价值", "安全边际"],
    "ROIC": ["ROIC", "资本回报率"],
    "巴菲特": ["巴菲特", "Buffett", "伯克希尔"],
    "芒格": ["芒格", "Munger"],
    "财务报表": ["财务报表", "财报", "利润表", "现金流量表", "资产负债表"],
    "估值": ["估值", "valuation"],
    "指数基金": ["指数基金", "ETF", "Vanguard"],
    "WACC": ["WACC", "加权平均资本成本"],
    "茅台": ["茅台"],
    "腾讯": ["腾讯"],
    "阿里巴巴": ["阿里巴巴", "阿里"],
    "美团": ["美团"],
    "拼多多": ["拼多多", "黄峥"],
    "香港": ["香港", "港股"],
    "A股": ["A股"],
    "AI": ["AI", "GPT", "人工智能", "Claude"],
    "市盈率": ["市盈率", "P/E", "PE"],
    "消费": ["消费行业", "消费"],
}

# URL patterns to skip (WeChat logos, QR codes, emoji, etc.)
SKIP_IMAGE_PATTERNS = [
    "mmbiz.qlogo.cn",      # WeChat avatars
    "res.wx.qq.com",        # WeChat system resources
    "wxp.wxpay.cn",         # WeChat Pay
    "wx.qlogo.cn",          # QR code avatars
    "/qrcode",              # QR codes
    "/reward",              # Reward/tip images
    "pic.wxstat.com",       # Stats pixels
    "3rdimg.hitcount",      # Tracking pixels
    "width=\"0\"",          # Tracking pixels
    "height=\"0\"",         # Tracking pixels
]


# ==================
# WeChat Article Fetcher
# ==================

def fetch_wechat_article(url):
    """Fetch and parse a WeChat article."""
    print(f"📥 Fetching article: {url}")

    headers = {
        "User-Agent": WECHAT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Check for WeChat error pages (expired/invalid links)
    error_msg = soup.find("div", class_="weui-msg__title")
    if error_msg:
        err_text = error_msg.get_text(strip=True)
        print(f"❌ WeChat returned error: {err_text}")
        print("   The article link may be expired or invalid.")
        sys.exit(1)

    # Extract title
    title_el = soup.find("h1", class_="rich_media_title") or soup.find("h1")
    if not title_el:
        print("❌ Could not find article title. The page might not be a valid WeChat article.")
        print("   Try opening the URL in a browser to verify it works.")
        sys.exit(1)
    title = title_el.get_text(strip=True)

    # Extract publish date
    date = None
    # Try <em id="publish_time">
    pub_time_el = soup.find("em", id="publish_time")
    if pub_time_el:
        date_text = pub_time_el.get_text(strip=True)
        date = _parse_date(date_text)
    # Try meta tag
    if not date:
        meta_time = soup.find("meta", property="article:published_time")
        if meta_time:
            date = _parse_date(meta_time.get("content", ""))
    # Fallback: look in script for var ct (create_time)
    if not date:
        for script in soup.find_all("script"):
            text = script.string or ""
            match = re.search(r'var\s+ct\s*=\s*"(\d+)"', text)
            if match:
                ts = int(match.group(1))
                date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                break
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Extract article body HTML
    content_el = soup.find("div", class_="rich_media_content") or soup.find("div", id="js_content")
    if not content_el:
        print("❌ Could not find article content element.")
        print("   WeChat may have blocked scraping. Try again later or use a different approach.")
        sys.exit(1)

    # Collect image URLs (handle WeChat lazy loading: data-src)
    images = []
    for img in content_el.find_all("img"):
        src = img.get("data-src") or img.get("src") or ""
        if not src or src.startswith("data:"):
            continue
        if any(pat in src for pat in SKIP_IMAGE_PATTERNS):
            continue
        # Check for tiny tracking pixels via width/height attributes
        w = img.get("data-w") or img.get("width") or ""
        h = img.get("data-h") or img.get("height") or ""
        if w and str(w).isdigit() and int(w) < 5:
            continue
        if h and str(h).isdigit() and int(h) < 5:
            continue
        images.append(src)

    return {
        "title": title,
        "date": date,
        "html": str(content_el),
        "images": images,
        "url": url,
    }


def _parse_date(text):
    """Try to parse a date string into YYYY-MM-DD."""
    text = text.strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text[:10], fmt[:min(len(fmt), 10)]).strftime("%Y-%m-%d")
        except (ValueError, IndexError):
            continue
    # Try ISO format with timezone
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass
    return None


# ==================
# HTML → Markdown Converter
# ==================

class WeChatConverter(MarkdownConverter):
    """Custom markdownify converter for WeChat articles."""

    def __init__(self, image_map=None, **kwargs):
        self.image_map = image_map or {}
        super().__init__(**kwargs)

    def convert_img(self, el, text, **kwargs):
        """Replace image URLs with local filenames."""
        src = el.get("data-src") or el.get("src") or ""
        local_name = self.image_map.get(src, "")
        if local_name:
            alt = el.get("alt", "")
            return f"\n\n![{alt}]({local_name})\n\n"
        return ""

    def convert_section(self, el, text, **kwargs):
        """Treat <section> as a div (pass through)."""
        return text

    def convert_span(self, el, text, **kwargs):
        """Clean up WeChat's excessive span wrapping."""
        return text


def html_to_markdown(html, image_map=None):
    """Convert WeChat HTML to clean Markdown."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove WeChat-specific junk elements
    for tag in soup.find_all(["style", "script", "iframe"]):
        tag.decompose()
    # Remove empty paragraphs / sections with only whitespace
    for tag in soup.find_all(["p", "section", "span"]):
        if not tag.get_text(strip=True) and not tag.find("img"):
            tag.decompose()

    converter = WeChatConverter(
        image_map=image_map or {},
        heading_style="atx",
        bullets="-",
        strip=["div", "section"],
    )
    md = converter.convert(str(soup))

    # Clean up: collapse excessive blank lines
    md = re.sub(r'\n{3,}', '\n\n', md)
    # Remove trailing whitespace on each line
    md = '\n'.join(line.rstrip() for line in md.split('\n'))
    # Strip leading/trailing whitespace
    md = md.strip()

    return md


# ==================
# Image Downloader
# ==================

def download_images(image_urls, dest_dir, dry_run=False):
    """Download images and return a mapping of URL → local filename."""
    image_map = {}
    if not image_urls:
        return image_map

    for i, url in enumerate(image_urls, 1):
        # Determine file extension from URL or Content-Type
        ext = _guess_extension(url)
        local_name = f"img_{i}{ext}"

        if dry_run:
            image_map[url] = local_name
            print(f"  📷 [dry-run] Would download: {local_name}")
            continue

        try:
            resp = requests.get(url, headers={"User-Agent": WECHAT_UA}, timeout=20)
            resp.raise_for_status()

            # Refine extension from Content-Type if URL didn't give us one
            if ext == ".jpg":
                ct = resp.headers.get("Content-Type", "")
                if "png" in ct:
                    ext = ".png"
                    local_name = f"img_{i}{ext}"
                elif "gif" in ct:
                    ext = ".gif"
                    local_name = f"img_{i}{ext}"
                elif "webp" in ct:
                    ext = ".webp"
                    local_name = f"img_{i}{ext}"

            filepath = dest_dir / local_name
            filepath.write_bytes(resp.content)
            image_map[url] = local_name
            print(f"  📷 Downloaded: {local_name} ({len(resp.content) // 1024}KB)")

        except Exception as e:
            print(f"  ⚠️  Failed to download image {i}: {e}")
            image_map[url] = local_name  # Still map it so markdown reference exists

    return image_map


def _guess_extension(url):
    """Guess image extension from URL."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    if ".png" in path:
        return ".png"
    elif ".gif" in path:
        return ".gif"
    elif ".webp" in path:
        return ".webp"
    elif ".jpeg" in path or ".jpg" in path:
        return ".jpg"
    # WeChat mmbiz URLs often use wx_fmt parameter
    if "wx_fmt=png" in url:
        return ".png"
    elif "wx_fmt=gif" in url:
        return ".gif"
    elif "wx_fmt=webp" in url:
        return ".webp"
    elif "wx_fmt=jpeg" in url or "wx_fmt=jpg" in url:
        return ".jpg"
    return ".jpg"  # Default


# ==================
# Slug & Tag Generators
# ==================

def slugify(title):
    """Generate a URL-friendly slug from a Chinese/English title.
    Reuses logic from import_notion.py — preserves Chinese characters.
    """
    slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = slug.lower()
    return slug


def generate_tags(title, content):
    """Generate tags based on keyword detection in title + content."""
    tags = []
    full_text = title + " " + content
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw in full_text:
                tags.append(tag)
                break
    return tags


# ==================
# AI Summary Generation
# ==================

def generate_summary(title, markdown_content):
    """Generate a concise Chinese summary using Claude API.
    Returns summary string, or empty string if unavailable.
    """
    try:
        import anthropic
    except ImportError:
        return ""

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return ""

    print("  📝 Generating summary via Claude API...")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""为以下中文博客文章生成一句话摘要（summary），用于SEO和首页展示。

要求：
1. 一句话，40-80个中文字符
2. 概括文章核心内容和价值
3. 使用客观描述性语言，不要用"本文"开头
4. 直接输出摘要，不要加引号或其他说明

文章标题: {title}

文章内容:
{markdown_content[:3000]}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        summary = message.content[0].text.strip().strip('"').strip("'")
        print(f"  ✅ Summary: {summary}")
        return summary
    except Exception as e:
        print(f"  ⚠️  Summary generation failed: {e}")
        return ""


# ==================
# Translation (Claude API)
# ==================

def translate_article(title, markdown_content, category_zh, tags_zh):
    """Translate Chinese article to English using Claude API.
    Returns (en_title, en_content, en_category, en_tags) or None if unavailable.
    """
    try:
        import anthropic
    except ImportError:
        print("  ⚠️  anthropic package not installed. Skipping translation.")
        print("     Install with: pip install anthropic")
        return None

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("  ⚠️  ANTHROPIC_API_KEY not set. Skipping translation.")
        return None

    # Map category
    en_category = CATEGORY_MAP.get(category_zh, "Business Analysis")

    # Map tags (simple Chinese → English mapping for common ones)
    tag_en_map = {
        "DCF": "DCF",
        "价值投资": "Value Investing",
        "ROIC": "ROIC",
        "巴菲特": "Buffett",
        "芒格": "Munger",
        "财务报表": "Financial Statements",
        "估值": "Valuation",
        "指数基金": "Index Funds",
        "WACC": "WACC",
        "茅台": "Moutai",
        "腾讯": "Tencent",
        "阿里巴巴": "Alibaba",
        "美团": "Meituan",
        "拼多多": "Pinduoduo",
        "香港": "Hong Kong",
        "A股": "A-Shares",
        "AI": "AI",
        "市盈率": "P/E Ratio",
        "消费": "Consumer",
    }
    en_tags = [tag_en_map.get(t, t) for t in tags_zh]

    print("  🌐 Translating to English via Claude API...")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Translate the following Chinese blog article into English.

Rules:
1. Translate the title and the full article body.
2. Write a one-sentence English summary (50-100 characters) for SEO.
3. Keep all Markdown formatting (headings, lists, bold, links, images) intact.
4. Do NOT translate image filenames in ![alt](filename) — keep the filenames exactly as-is.
5. Maintain the same paragraph structure and tone.
6. For proper nouns (company names, people), use their common English names.
7. Output ONLY the translation, no explanations.

Format your response as:
TITLE: <translated title>
SUMMARY: <one-sentence English summary>
---
<translated article body in Markdown>

---

Chinese Title: {title}

Chinese Article:
{markdown_content}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = message.content[0].text

        # Parse response
        lines = response_text.split("\n")
        en_title = ""
        en_summary = ""
        body_start = 0

        for i, line in enumerate(lines):
            if line.startswith("TITLE:"):
                en_title = line[6:].strip().strip('"')
            elif line.startswith("SUMMARY:"):
                en_summary = line[8:].strip().strip('"')
            elif line.strip() == "---":
                body_start = i + 1
                break

        en_content = "\n".join(lines[body_start:]).strip()

        if not en_title:
            en_title = lines[0].strip().strip("#").strip()
        if not en_content:
            en_content = response_text

        print(f"  ✅ Translation complete: \"{en_title}\"")
        return en_title, en_content, en_category, en_tags, en_summary

    except Exception as e:
        print(f"  ⚠️  Translation failed: {e}")
        return None


# ==================
# Hugo Page Bundle Creator
# ==================

def create_zh_bundle(slug, title, date, category, content, dest_dir, summary="", dry_run=False):
    """Create the Chinese page bundle."""
    bundle_dir = dest_dir / slug

    # Front matter (matching existing zh posts)
    summary_line = f'\nsummary: "{summary}"' if summary else ""
    front_matter = f"""---
title: "{title}"
date: {date}
categories:
  - {category}{summary_line}
---"""

    full_content = front_matter + "\n\n" + content + "\n"

    if dry_run:
        print(f"\n📁 [dry-run] Would create: {bundle_dir}/index.md")
        print(f"   Title: {title}")
        print(f"   Date: {date}")
        print(f"   Category: {category}")
        print(f"   Content length: {len(content)} chars")
        return bundle_dir

    bundle_dir.mkdir(parents=True, exist_ok=True)
    (bundle_dir / "index.md").write_text(full_content, encoding="utf-8")
    print(f"  ✅ Created: {bundle_dir}/index.md")
    return bundle_dir


def create_en_bundle(slug, title, date, category, tags, content, dest_dir, summary="", dry_run=False):
    """Create the English page bundle."""
    bundle_dir = dest_dir / slug

    tags_str = ", ".join(f'"{t}"' for t in tags)
    front_matter = f"""---
title: "{title}"
date: {date}
draft: false
slug: "{slug}"
categories: ["{category}"]
tags: [{tags_str}]
summary: "{summary}"
---"""

    full_content = front_matter + "\n\n" + content + "\n"

    if dry_run:
        print(f"\n📁 [dry-run] Would create: {bundle_dir}/index.md")
        print(f"   Title: {title}")
        print(f"   Category: {category}")
        print(f"   Tags: {tags}")
        return bundle_dir

    bundle_dir.mkdir(parents=True, exist_ok=True)
    (bundle_dir / "index.md").write_text(full_content, encoding="utf-8")
    print(f"  ✅ Created: {bundle_dir}/index.md")
    return bundle_dir


def copy_images_to_en(zh_bundle_dir, en_bundle_dir, dry_run=False):
    """Copy images from zh bundle to en bundle."""
    if not zh_bundle_dir.exists():
        return

    en_bundle_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in zh_bundle_dir.iterdir():
        if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            if dry_run:
                print(f"  📷 [dry-run] Would copy: {f.name} → en")
            else:
                shutil.copy2(f, en_bundle_dir / f.name)
            count += 1

    if count and not dry_run:
        print(f"  📷 Copied {count} images to English bundle")


# ==================
# Main
# ==================

def interactive_mode():
    """Run in interactive mode — prompt for URL and category."""
    print("=" * 50)
    print("  见山笔记 — 微信文章导入工具")
    print("=" * 50)

    # Prompt for URL
    print()
    url = input("📎 粘贴微信文章链接: ").strip()
    if not url:
        print("❌ 未输入链接，退出。")
        sys.exit(1)

    # Show category options
    categories = list(CATEGORY_MAP.keys())
    print("\n📂 选择分类:")
    for i, cat in enumerate(categories, 1):
        print(f"   {i}. {cat}")
    print(f"   {len(categories) + 1}. 自定义")

    choice = input(f"\n   输入编号 [默认 1]: ").strip()
    if not choice or choice == "1":
        category = categories[0]
    elif choice.isdigit() and 1 <= int(choice) <= len(categories):
        category = categories[int(choice) - 1]
    elif choice.isdigit() and int(choice) == len(categories) + 1:
        category = input("   输入自定义分类: ").strip() or "商业分析"
    else:
        category = categories[0]

    print(f"\n   → 分类: {category}")

    # Ask about translation
    translate = input("\n🌐 翻译为英文? [Y/n]: ").strip().lower()
    no_translate = translate in ("n", "no")

    print()
    return url, category, no_translate


def main():
    parser = argparse.ArgumentParser(
        description="Import a WeChat article into the Hugo blog",
        epilog="Example: python scripts/publish.py 'https://mp.weixin.qq.com/s/xxx' --category '公司估值'",
    )
    parser.add_argument("url", nargs="?", default=None, help="WeChat article URL (omit for interactive mode)")
    parser.add_argument("--category", default="商业分析", help="Category name in Chinese (default: 商业分析)")
    parser.add_argument("--date", default=None, help="Override publish date (YYYY-MM-DD)")
    parser.add_argument("--no-translate", action="store_true", help="Skip English translation")
    parser.add_argument("--no-images", action="store_true", help="Skip image downloads")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")

    args = parser.parse_args()

    # Interactive mode if no URL provided
    if not args.url:
        url, category, no_translate = interactive_mode()
        args.url = url
        args.category = category
        args.no_translate = no_translate

    # Validate URL
    if "mp.weixin.qq.com" not in args.url and "weixin.qq.com" not in args.url:
        print("⚠️  URL does not look like a WeChat article. Proceeding anyway...")

    # Step 1: Fetch article
    article = fetch_wechat_article(args.url)
    title = article["title"]
    date = args.date or article["date"]
    slug = slugify(title)

    print(f"\n📄 Article: {title}")
    print(f"   Date: {date}")
    print(f"   Slug: {slug}")
    print(f"   Images found: {len(article['images'])}")
    print(f"   Category: {args.category}")

    # Step 2: Download images
    zh_bundle_dir = ZH_POSTS_DIR / slug
    if args.no_images:
        image_map = {}
        print("\n⏭️  Skipping image downloads")
    else:
        print("\n📷 Downloading images...")
        if not args.dry_run:
            zh_bundle_dir.mkdir(parents=True, exist_ok=True)
        image_map = download_images(article["images"], zh_bundle_dir, dry_run=args.dry_run)

    # Step 3: Convert HTML → Markdown
    print("\n📝 Converting HTML to Markdown...")
    markdown_content = html_to_markdown(article["html"], image_map=image_map)

    # Step 4: Generate tags
    tags_zh = generate_tags(title, markdown_content)
    print(f"   Auto-detected tags: {tags_zh}")

    # Step 5: Generate AI summary
    print("\n📝 Generating summary...")
    zh_summary = generate_summary(title, markdown_content)

    # Step 6: Create Chinese page bundle
    print("\n🇨🇳 Creating Chinese article...")
    create_zh_bundle(slug, title, date, args.category, markdown_content, ZH_POSTS_DIR, summary=zh_summary, dry_run=args.dry_run)

    # Step 7: Translate and create English page bundle
    if args.no_translate:
        print("\n⏭️  Skipping English translation")
    else:
        print("\n🇬🇧 Creating English article...")
        result = translate_article(title, markdown_content, args.category, tags_zh)
        if result:
            en_title, en_content, en_category, en_tags, en_summary = result
            create_en_bundle(slug, en_title, date, en_category, en_tags, en_content, EN_POSTS_DIR, summary=en_summary, dry_run=args.dry_run)
            copy_images_to_en(zh_bundle_dir, EN_POSTS_DIR / slug, dry_run=args.dry_run)
        else:
            print("  ⚠️  Skipped English version (translation unavailable)")

    # Summary
    print(f"\n{'='*50}")
    if args.dry_run:
        print("✅ Dry run complete. No files were written.")
    else:
        print("✅ Import complete!")
        print(f"   Chinese: content/zh/posts/{slug}/index.md")
        if not args.no_translate:
            print(f"   English: content/en/posts/{slug}/index.md")
        print(f"\n   Preview with: hugo server -D")
        print(f"   Then commit:  git add content/ && git commit -m 'Add post: {title}'")


if __name__ == "__main__":
    main()
