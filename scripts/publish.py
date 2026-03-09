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
import json
import mimetypes
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta
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
# Valuation Article Generator
# ==================

VALUX_DB_PATH = os.environ.get("VALUX_DB_PATH", str(Path.home() / "valux" / "valuations.db"))
FMP_API_KEY = os.environ.get("FMP_API_KEY", "")

# Chinese name → ticker mapping for companies with English names in the DB
CHINESE_TICKER_MAP = {
    "快手": "1024.HK",
    "泡泡玛特": "9992.HK",
    "阅文": "0772.HK",
    "大麦": "1060.HK",
    "英伟达": "NVDA",
    "奈飞": "NFLX",
}


def load_valuation(query):
    """Load latest valuation from ValuX-DB by ticker or company name.
    Returns dict with all valuation data or None.
    """
    db_path = VALUX_DB_PATH
    if not Path(db_path).exists():
        print(f"❌ ValuX database not found: {db_path}")
        return None

    # Resolve Chinese alias to ticker
    resolved = CHINESE_TICKER_MAP.get(query, query)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Try exact ticker match first, then fuzzy company name
    cur.execute(
        "SELECT * FROM valuations WHERE ticker = ? ORDER BY valuation_date DESC LIMIT 1",
        (resolved.upper(),),
    )
    row = cur.fetchone()

    if not row:
        cur.execute(
            "SELECT * FROM valuations WHERE company_name LIKE ? ORDER BY valuation_date DESC LIMIT 1",
            (f"%{query}%",),
        )
        row = cur.fetchone()

    if not row:
        # Try FTS
        cur.execute(
            "SELECT v.* FROM valuations v JOIN valuations_fts f ON v.id = f.rowid "
            "WHERE valuations_fts MATCH ? ORDER BY v.valuation_date DESC LIMIT 1",
            (query,),
        )
        row = cur.fetchone()

    conn.close()

    if not row:
        print(f"❌ No valuation found for: {query}")
        return None

    data = dict(row)

    # Parse JSON fields
    for field in ("sensitivity_json", "summary_json", "ai_parameters_json",
                  "wacc_sensitivity_json", "dcf_table_json"):
        if data.get(field):
            try:
                data[field] = json.loads(data[field])
            except (json.JSONDecodeError, TypeError):
                pass

    print(f"  ✅ Loaded valuation: {data['company_name']} ({data['ticker']}) — {data['valuation_date']}")
    return data


def get_current_price(ticker):
    """Fetch real-time price from FMP API. Returns (price, currency) or (None, None)."""
    if not FMP_API_KEY:
        print("  ⚠️  FMP_API_KEY not set, using valuation market_price")
        return None, None

    # Map exchange suffix to FMP format
    fmp_ticker = ticker
    if ticker.endswith(".HK"):
        fmp_ticker = ticker.replace(".HK", ".HK")  # FMP uses same format
    elif ticker.endswith(".SS"):
        fmp_ticker = ticker.replace(".SS", ".SS")
    elif ticker.endswith(".SZ"):
        fmp_ticker = ticker.replace(".SZ", ".SZ")
    elif ticker.endswith(".T"):
        fmp_ticker = ticker.replace(".T", ".T")

    url = f"https://financialmodelingprep.com/api/v3/quote-short/{fmp_ticker}?apikey={FMP_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data and len(data) > 0:
            price = data[0].get("price")
            print(f"  📊 Current price: {price}")
            return price, None
    except Exception as e:
        print(f"  ⚠️  FMP price fetch failed: {e}")

    return None, None


def reverse_engineer_market_expectations(sensitivity_json, current_price):
    """Find the iso-price curve in the sensitivity matrix for the current stock price.

    The sensitivity matrix is 2D (revenue_growth × ebit_margin → price).
    A single stock price can correspond to many (growth, margin) combinations.
    Instead of pretending there's one "market-implied" point, we find all
    combinations that produce prices close to the current price — the iso-price
    curve — and let the article discuss which scenarios are more plausible.

    Returns dict with:
      - iso_curve: list of (growth, margin, price) tuples near current price
      - range_low/range_high: middle 50% of all prices in the matrix
    """
    if not sensitivity_json or not current_price:
        return None

    # For each growth rate, find the margin that produces the closest price
    # to current_price. Include if within 10% tolerance.
    tolerance = current_price * 0.10
    iso_curve = []

    for g_str, margins in sorted(sensitivity_json.items(), key=lambda x: float(x[0])):
        if not isinstance(margins, dict):
            continue
        best_m, best_diff, best_p = None, float("inf"), None
        for m_str, price in margins.items():
            try:
                diff = abs(float(price) - current_price)
                if diff < best_diff:
                    best_diff = diff
                    best_m = float(m_str)
                    best_p = float(price)
            except (ValueError, TypeError):
                continue
        if best_m is not None and best_diff <= tolerance:
            iso_curve.append({
                "growth": float(g_str),
                "margin": best_m,
                "price": best_p,
            })

    # Compute valuation range from matrix
    all_prices = []
    for margins in sensitivity_json.values():
        if isinstance(margins, dict):
            for price in margins.values():
                try:
                    all_prices.append(float(price))
                except (ValueError, TypeError):
                    continue

    result = {"iso_curve": iso_curve}
    if all_prices:
        all_prices.sort()
        result["matrix_low"] = all_prices[0]
        result["matrix_high"] = all_prices[-1]
        q1 = all_prices[len(all_prices) // 4]
        q3 = all_prices[3 * len(all_prices) // 4]
        result["range_low"] = q1
        result["range_high"] = q3

    # Log
    if iso_curve:
        print(f"  🔍 Found {len(iso_curve)} combinations near current price:")
        for pt in iso_curve:
            print(f"      growth {pt['growth']:.0f}% + margin {pt['margin']:.0f}% → {pt['price']:.0f}")
    if "range_low" in result:
        print(f"  🔍 Sensitivity range (Q1-Q3): {result['range_low']:.0f} - {result['range_high']:.0f}")

    return result if result else None


def _call_claude_cli(prompt, max_tokens=4000):
    """Call the claude CLI via subprocess. Returns response text or None.

    Uses the claude CLI which handles auth via Claude Code / Max subscription,
    avoiding the need for ANTHROPIC_API_KEY.
    """
    claude_path = shutil.which("claude")
    if not claude_path:
        print("  ❌ claude CLI not found. Install Claude Code first.")
        return None

    cmd = [claude_path, "-p", prompt, "--output-format", "json"]

    # Clean environment to avoid "nested session" errors when run from Claude Code
    clean_env = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE")}
    clean_env["PATH"] = os.environ.get("PATH", "/usr/bin:/usr/local/bin")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=600, env=clean_env, encoding="utf-8", errors="replace",
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()[:500] if result.stderr else ""
            print(f"  ❌ claude CLI error (exit {result.returncode}): {stderr}")
            return None

        raw = result.stdout.strip()
        if not raw:
            print("  ❌ claude CLI returned empty output")
            return None

        # Parse JSON response
        try:
            data = json.loads(raw)
            text = data.get("result", raw)
            # Log model used
            if "modelUsage" in data:
                models = data["modelUsage"]
                primary = max(models, key=lambda m: models[m].get("costUSD", 0))
                print(f"  🤖 Model: {primary}")
            return text.strip()
        except (json.JSONDecodeError, KeyError):
            # If not JSON, return raw output
            return raw.strip()

    except subprocess.TimeoutExpired:
        print("  ❌ claude CLI timed out (10 min)")
        return None
    except Exception as e:
        print(f"  ❌ claude CLI failed: {e}")
        return None


def generate_valuation_article(valuation_data, current_price, market_expectations):
    """Generate article via claude CLI. Returns markdown string."""
    v = valuation_data
    ticker = v["ticker"]
    company = v["company_name"]
    dcf_price = v.get("price_per_share", 0)
    gap_pct = v.get("gap_pct", 0)
    currency = v.get("currency", "HKD")

    # Build financial history summary
    fin_history = ""
    if isinstance(v.get("summary_json"), dict):
        for year, metrics in sorted(v["summary_json"].items()):
            if isinstance(metrics, dict):
                rev = metrics.get("Revenue", "N/A")
                ebit = metrics.get("EBIT", "N/A")
                ebit_m = metrics.get("EBIT Margin (%)", "N/A")
                rev_g = metrics.get("Revenue Growth (%)", "N/A")
                period = metrics.get("Period", year)
                fin_history += f"- {period}: 收入 {rev}, EBIT {ebit}, EBIT利润率 {ebit_m}%, 收入增速 {rev_g}%\n"

    # Build AI reasoning
    ai_reasoning = ""
    if isinstance(v.get("ai_parameters_json"), dict):
        for param, info in v["ai_parameters_json"].items():
            if isinstance(info, dict):
                val = info.get("value", "N/A")
                reason = info.get("reasoning", "")
                ai_reasoning += f"- {param}: {val} — {reason[:200]}\n"

    # Market expectations — iso-price curve
    mkt_exp = ""
    if market_expectations:
        me = market_expectations
        iso = me.get("iso_curve", [])
        if iso:
            mkt_exp += "当前股价在敏感性矩阵中对应以下几组等价假设（这些组合都能解释当前价格）：\n"
            for pt in iso:
                mkt_exp += f"- 收入增速 {pt['growth']:.0f}% + EBIT利润率 {pt['margin']:.0f}% → 约{pt['price']:.0f} {currency}\n"
            mkt_exp += "\n关键问题：这些情景中，哪个更接近现实？\n"
        if "range_low" in me:
            mkt_exp += f"敏感性矩阵中间区间: {me['range_low']:.0f} - {me['range_high']:.0f} {currency}\n"

    # Gap analysis
    gap_text = v.get("gap_analysis_text", "") or ""
    if len(gap_text) > 2000:
        gap_text = gap_text[:2000] + "..."

    # DCF key params
    rg1 = v.get("revenue_growth_1", "N/A")
    rg2 = v.get("revenue_growth_2", "N/A")
    em = v.get("ebit_margin", "N/A")
    wacc = v.get("wacc", "N/A")

    # Approximate DCF price (round to nearest 5)
    dcf_approx = round(dcf_price / 5) * 5

    # Determine safety margin direction
    if gap_pct and gap_pct > 0:
        safety_label = f"低估约{abs(gap_pct):.0f}%"
    elif gap_pct and gap_pct < 0:
        safety_label = f"高估约{abs(gap_pct):.0f}%"
    else:
        safety_label = "大致合理"

    prompt = f"""你是「见山笔记」的作者，写关于 {company}（{ticker}）的投资分析文章。

最重要的一条：用商业问题来组织文章，每个DCF假设都应该是一个商业问题的自然回答。
不要把"讲生意"和"讲估值"分开——它们是一体的。比如不要先花三段讲竞争格局，再另起一段说"所以利润率假设是50%"。
而是像这样组织：提出一个读者关心的商业问题（"增长还能撑多久？""利润率能守住吗？"），然后在回答这个问题的过程中，自然地把估值假设和业务逻辑编织在一起。

写作原则：
- 像聊天不像研报，段落标题用问句，过渡自然
- 「模糊的正确胜于精确的错误」——给区间，不强调精确数字
- 每个关键DCF假设（增速、利润率等）第一次出现时，要让读者知道这是估值里用的数——但用自然的方式，比如"DCF里给的长期增速是20%""估值取的成熟期利润率是50%"，说一次就够了，之后再提到同一个数字可以直接用
- 文章开头或前两段就要给出DCF估值结果作为锚点（约XX元），让读者带着这个数字往下读，不要全篇讲假设最后才揭晓结论
- 少用"我""我们"；不用：值得注意的是、总而言之、综上所述、emoji

## 数据

当前市价: {current_price} {currency} | DCF估值: 约{dcf_approx} {currency}（{safety_label}）

近几年财务：
{fin_history}

DCF假设：Y1增速 {rg1}%，Y2-5复合增速 {rg2}%，EBIT利润率 {em}%，WACC {wacc}%
假设理由：
{ai_reasoning}

等价曲线（当前股价对应的多组假设）：
{mkt_exp}

差异分析：
{gap_text}

## 输出

第一行 # 标题（有吸引力，适合自媒体），然后文章正文。
结尾加一行免责声明（例：*免责声明：本文仅为个人研究记录，不构成投资建议。*）。
全文控制在800-1200字，宁短勿长，每段点到为止。
只输出文章本身，不要加代码块、YAML、front matter、说明或改动对比。"""

    print("  ✍️  Generating article via Claude CLI...")
    article = _call_claude_cli(prompt)
    if article:
        print(f"  ✅ Article generated ({len(article)} chars)")
    return article


def check_dedup(ticker, company_name):
    """Check if a post for this ticker exists within the last 30 days.
    Returns the existing slug or None.
    """
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    # Search in zh posts directory
    for post_dir in ZH_POSTS_DIR.iterdir():
        if not post_dir.is_dir():
            continue
        index_file = post_dir / "index.md"
        if not index_file.exists():
            continue

        dir_name = post_dir.name.lower()
        # Check if ticker or company name appears in slug
        ticker_short = ticker.split(".")[0].lower()
        if ticker_short in dir_name or company_name.lower()[:4] in dir_name:
            # Check date in front matter
            try:
                content = index_file.read_text(encoding="utf-8")
                date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", content)
                if date_match and date_match.group(1) >= cutoff:
                    return post_dir.name
            except Exception:
                continue

    return None


def run_valuation(args):
    """Main flow for the valuation subcommand."""
    query = args.query
    print(f"\n{'='*50}")
    print(f"  见山笔记 — 估值文章生成")
    print(f"{'='*50}")

    # Step 1: Load valuation from DB
    print(f"\n📊 Loading valuation for: {query}")
    valuation = load_valuation(query)
    if not valuation:
        sys.exit(1)

    ticker = valuation["ticker"]
    company = valuation["company_name"]
    dcf_price = valuation.get("price_per_share", 0)
    gap_pct = valuation.get("gap_pct", 0)
    currency = valuation.get("currency", "HKD")

    # Step 2: Get current price
    print(f"\n💰 Fetching current price for {ticker}...")
    current_price, _ = get_current_price(ticker)
    if not current_price:
        current_price = valuation.get("market_price", 0)
        print(f"  📊 Using valuation market price: {current_price}")

    # Step 3: Reverse-engineer market expectations (iso-price curve)
    print(f"\n🔍 Analyzing market expectations...")
    market_exp = reverse_engineer_market_expectations(
        valuation.get("sensitivity_json"), current_price
    )

    # Step 4: Check dedup
    existing = check_dedup(ticker, company)
    if existing and not args.dry_run:
        print(f"\n⚠️  Found existing post within 30 days: {existing}")
        answer = input("   Create new anyway? [y/N]: ").strip().lower()
        if answer not in ("y", "yes"):
            print("   Aborted.")
            sys.exit(0)

    # Step 5: Generate article (Claude also generates the title)
    print(f"\n✍️  Generating article...")
    raw_output = generate_valuation_article(valuation, current_price, market_exp)
    if not raw_output:
        sys.exit(1)

    # Parse title from Claude output (first H1 line) and clean artifacts
    lines = raw_output.split("\n")
    title = None
    article_lines = []
    in_code_block = False
    skip_trailing = False
    for line in lines:
        # Track fenced code blocks to skip YAML front matter blocks
        if line.strip().startswith("```"):
            if not in_code_block:
                # Starting a code block — skip if it looks like YAML front matter
                lower = line.strip().lower()
                if any(k in lower for k in ("yaml", "front", "matter")):
                    in_code_block = True
                    continue
                # Also skip generic ``` blocks that appear before any real content
                if not article_lines or all(l.strip() == "" for l in article_lines):
                    in_code_block = True
                    continue
            else:
                in_code_block = False
                continue
        if in_code_block:
            continue
        # Skip trailing meta-commentary (e.g. "相比旧版的主要改动")
        if skip_trailing:
            continue
        if re.match(r"^(---|###?\s*(相比|改动|变化|修改|注[：:]|说明))", line):
            skip_trailing = True
            continue
        # Extract title from first H1
        if title is None and line.startswith("# "):
            title = line[2:].strip()
        else:
            article_lines.append(line)
    article_content = "\n".join(article_lines).strip()
    # Remove any remaining front-matter-like block at the start
    article_content = re.sub(r"^---\n.*?\n---\n*", "", article_content, flags=re.DOTALL)

    if not title:
        # Fallback title
        dcf_approx = round(dcf_price / 5) * 5  # round to nearest 5
        title = f"{company}值多少钱？DCF估值约{dcf_approx} {currency}"

    date = args.date or datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    category = "公司估值"

    # Step 7: Tags — keep it simple
    tags_zh = ["估值"]

    # Step 8: Preview
    print(f"\n{'='*50}")
    print(f"📄 Preview")
    print(f"{'='*50}")
    print(f"   Title:    {title}")
    print(f"   Date:     {date}")
    print(f"   Slug:     {slug}")
    print(f"   Category: {category}")
    print(f"   Tags:     {tags_zh}")
    dcf_approx = round(dcf_price / 5) * 5
    print(f"   Ticker:   {ticker} @ {current_price} {currency}")
    print(f"   DCF:      ~{dcf_approx} {currency} (gap {gap_pct:+.0f}%)" if gap_pct else f"   DCF:      ~{dcf_approx} {currency}")
    print(f"\n{'─'*50}")
    print(article_content)
    print(f"{'─'*50}")

    if args.dry_run:
        print(f"\n✅ Dry run complete. No files written.")
        return

    # Step 9: Edit or confirm
    import tempfile
    while True:
        action = input(f"\n  [p]ublish / [e]dit / [q]uit: ").strip().lower()
        if action in ("q", "quit", "n", "no"):
            print("   Aborted.")
            return
        elif action in ("e", "edit"):
            # Write current article (with title as H1) to temp file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", prefix="valuation_", delete=False, encoding="utf-8"
            ) as f:
                f.write(f"# {title}\n\n{article_content}\n")
                tmp_path = f.name
            # Open in GUI editor
            subl_path = shutil.which("subl") or "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"
            if Path(subl_path).exists():
                os.system(f'"{subl_path}" "{tmp_path}"')
            elif shutil.which("code"):
                os.system(f'code "{tmp_path}"')
            elif sys.platform == "darwin":
                os.system(f'open -e "{tmp_path}"')
            else:
                editor = os.environ.get("EDITOR", "nano")
                os.system(f'{editor} "{tmp_path}"')
            input("  📝 在编辑器中修改，保存(⌘S)后回到这里按回车继续...")
            # Read back edited content
            edited = Path(tmp_path).read_text(encoding="utf-8")
            os.unlink(tmp_path)
            # Re-parse title and content
            edited_lines = edited.split("\n")
            title = None
            article_lines = []
            for line in edited_lines:
                if title is None and line.startswith("# "):
                    title = line[2:].strip()
                else:
                    article_lines.append(line)
            article_content = "\n".join(article_lines).strip()
            if not title:
                title = f"{company}值多少钱？"
            slug = slugify(title)
            # Show updated preview
            print(f"\n{'='*50}")
            print(f"📄 Updated Preview")
            print(f"{'='*50}")
            print(f"   Title:    {title}")
            print(f"   Slug:     {slug}")
            print(f"\n{'─'*50}")
            print(article_content)
            print(f"{'─'*50}")
            continue
        elif action in ("p", "publish", "y", "yes"):
            break
        else:
            if action == "":
                continue  # ignore empty Enter
            print("   Invalid choice. Use [p]ublish, [e]dit, or [q]uit.")
            continue

    # Step 10: Generate summary
    zh_summary = generate_summary(title, article_content)

    # Step 11: Create Chinese bundle
    print(f"\n🇨🇳 Creating Chinese article...")
    zh_dir = create_zh_bundle(slug, title, date, category, article_content, ZH_POSTS_DIR, summary=zh_summary)

    # Step 12: Translate and create English bundle
    if not args.no_translate:
        print(f"\n🇬🇧 Creating English article...")
        result = translate_article(title, article_content, category, tags_zh)
        if result:
            en_title, en_content, en_category, en_tags, en_summary = result
            create_en_bundle(slug, en_title, date, en_category, en_tags, en_content, EN_POSTS_DIR, summary=en_summary)
            copy_images_to_en(zh_dir, EN_POSTS_DIR / slug)
        else:
            print("  ⚠️  Skipped English version")
    else:
        print(f"\n⏭️  Skipping English translation")

    # Step 13: Git commit & push
    print(f"\n📦 Committing and pushing...")
    os.chdir(BLOG_ROOT)
    os.system(f'git add content/')
    os.system(f'git commit -m "Add valuation: {company} ({ticker})"')
    os.system(f'git push')

    # Step 14: Summary
    print(f"\n{'='*50}")
    print(f"✅ Published!")
    print(f"   Chinese: content/zh/posts/{slug}/index.md")
    if not args.no_translate:
        print(f"   English: content/en/posts/{slug}/index.md")
    print(f"   Preview: hugo server -D")


# ==================
# AI Summary Generation
# ==================

def generate_summary(title, markdown_content):
    """Generate a concise Chinese summary using claude CLI.
    Returns summary string, or empty string if unavailable.
    """
    print("  📝 Generating summary via Claude CLI...")

    prompt = f"""为以下中文博客文章生成一句话摘要（summary），用于SEO和首页展示。

要求：
1. 一句话，40-80个中文字符
2. 概括文章核心内容和价值
3. 使用客观描述性语言，不要用"本文"开头
4. 直接输出摘要，不要加引号或其他说明

文章标题: {title}

文章内容:
{markdown_content[:3000]}"""

    summary = _call_claude_cli(prompt)
    if summary:
        summary = summary.strip('"').strip("'")
        print(f"  ✅ Summary: {summary}")
        return summary
    print("  ⚠️  Summary generation failed")
    return ""


# ==================
# Translation (Claude API)
# ==================

def translate_article(title, markdown_content, category_zh, tags_zh):
    """Translate Chinese article to English using claude CLI.
    Returns (en_title, en_content, en_category, en_tags, en_summary) or None.
    """
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

    print("  🌐 Translating to English via Claude CLI...")

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

    response_text = _call_claude_cli(prompt)
    if not response_text:
        print("  ⚠️  Translation failed")
        return None

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
    # Route "valuation" subcommand before argparse (avoids positional arg conflicts)
    if len(sys.argv) > 1 and sys.argv[1] == "valuation":
        val_parser = argparse.ArgumentParser(
            prog="js valuation",
            description="Generate valuation article from ValuX-DB",
        )
        val_parser.add_argument("_cmd", help=argparse.SUPPRESS)  # consume "valuation"
        val_parser.add_argument("query", help="Ticker (e.g. NVDA, 1024.HK) or company name (e.g. 快手)")
        val_parser.add_argument("--date", default=None, help="Override publish date (YYYY-MM-DD)")
        val_parser.add_argument("--no-translate", action="store_true", help="Skip English translation")
        val_parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
        args = val_parser.parse_args()
        run_valuation(args)
        return

    parser = argparse.ArgumentParser(
        description="Import a WeChat article into the Hugo blog",
        epilog="Examples:\n"
               "  js 'https://mp.weixin.qq.com/s/xxx' --category '公司估值'\n"
               "  js valuation 快手\n"
               "  js valuation NVDA --dry-run",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", nargs="?", default=None, help="WeChat article URL (omit for interactive mode)")
    parser.add_argument("--category", default="商业分析", help="Category name in Chinese (default: 商业分析)")
    parser.add_argument("--date", default=None, help="Override publish date (YYYY-MM-DD)")
    parser.add_argument("--no-translate", action="store_true", help="Skip English translation")
    parser.add_argument("--no-images", action="store_true", help="Skip image downloads")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")

    args = parser.parse_args()

    # Default: WeChat import flow
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
