#!/usr/bin/env python3
"""
Migrate English post slugs from Chinese/mixed characters to clean English slugs.

For each content/en/posts/*/index.md:
  1. Parse YAML frontmatter
  2. Generate a clean English slug from the title
  3. If the new slug differs from the effective current URL slug
     (either the explicit `slug:` field or the folder name), update
     `slug:` to the new English slug and append the old URL path to
     `aliases:` so old links still resolve.

Hugo `aliases` generate meta-refresh redirect pages, which Google treats
as soft 301s.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

BLOG_ROOT = Path(__file__).resolve().parent.parent
EN_POSTS = BLOG_ROOT / "content" / "en" / "posts"

# Characters kept in slugs: a-z, 0-9, and hyphen.
_SLUG_SAFE = re.compile(r"[^a-z0-9]+")
# Words/symbols to drop from titles before slugging.
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "of", "for", "to", "in", "on",
    "at", "by", "from", "with", "is", "are", "was", "were", "be", "been",
    "it", "its", "as", "that", "this", "these", "those",
}
_MAX_SLUG_LEN = 60  # keep URLs tidy


def slugify(title: str) -> str:
    """Convert an English title into a URL slug.

    Drops punctuation, lowercases, removes short stopwords, collapses
    runs of non-alphanumerics into single dashes, and truncates at a
    word boundary.
    """
    # Normalize Unicode and strip combining marks so "Schrödinger" -> "Schrodinger".
    text = unicodedata.normalize("NFKD", title)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    # Remove apostrophes entirely so "buffett's" -> "buffetts", not "buffett-s".
    text = re.sub(r"[\u2019\u2018'`]", "", text)
    # Collapse "r&d" style ampersand words: drop "&" so "r&d" -> "rd".
    text = text.replace("&", "")
    # Replace remaining punctuation with spaces so word boundaries survive.
    text = re.sub(r"[—–\-_:;,.!?()\[\]{}\"/\\+]+", " ", text)
    words = [w for w in text.split() if w]
    # Drop stopwords but keep them if removing would leave too few words.
    trimmed = [w for w in words if w not in _STOPWORDS]
    if len(trimmed) >= 3:
        words = trimmed
    joined = " ".join(words)
    slug = _SLUG_SAFE.sub("-", joined).strip("-")
    if len(slug) <= _MAX_SLUG_LEN:
        return slug
    # Trim to the last full word within the length budget.
    cutoff = slug[:_MAX_SLUG_LEN].rsplit("-", 1)[0]
    return cutoff or slug[:_MAX_SLUG_LEN]


def parse_frontmatter(text: str) -> tuple[list[str], list[str]]:
    """Split a markdown file into (frontmatter_lines, body_lines).

    Assumes frontmatter is YAML fenced by `---` lines.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Missing opening YAML fence")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1 :]
    raise ValueError("Missing closing YAML fence")


def get_field(fm_lines: list[str], key: str) -> str | None:
    """Return the value of a top-level scalar YAML field or None."""
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*?)\s*$")
    for line in fm_lines:
        m = pattern.match(line)
        if m:
            value = m.group(1)
            # Strip surrounding quotes if present.
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            return value
    return None


def find_aliases_block(fm_lines: list[str]) -> tuple[int, int] | None:
    """Return (start_idx, end_idx_exclusive) of an existing aliases block."""
    for i, line in enumerate(fm_lines):
        if re.match(r"^aliases:\s*(\[.*\])?\s*$", line):
            # Inline list form: aliases: [a, b]
            if re.match(r"^aliases:\s*\[.*\]\s*$", line):
                return i, i + 1
            # Block list form: aliases: followed by "  - item" lines.
            end = i + 1
            while end < len(fm_lines) and re.match(r"^\s+-\s+", fm_lines[end]):
                end += 1
            return i, end
    return None


def ensure_alias_in_block(
    fm_lines: list[str], old_path: str
) -> list[str]:
    """Return frontmatter lines with `old_path` added to aliases."""
    block = find_aliases_block(fm_lines)
    if block is None:
        return fm_lines + [f'aliases:', f'  - "{old_path}"']
    start, end = block
    existing = "\n".join(fm_lines[start:end])
    if old_path in existing:
        return fm_lines
    # If the existing form is inline list, convert to block form.
    if re.match(r"^aliases:\s*\[.*\]\s*$", fm_lines[start]):
        inline = fm_lines[start]
        m = re.match(r"^aliases:\s*\[(.*)\]\s*$", inline)
        items = [x.strip().strip("\"'") for x in (m.group(1).split(",") if m else []) if x.strip()]
        items.append(old_path)
        new_lines = ["aliases:"] + [f'  - "{it}"' for it in items]
        return fm_lines[:start] + new_lines + fm_lines[end:]
    # Block form: append another "  - <old_path>" line at the end of the block.
    return fm_lines[:end] + [f'  - "{old_path}"'] + fm_lines[end:]


def update_slug_line(fm_lines: list[str], new_slug: str) -> list[str]:
    """Replace an existing `slug:` line or append one at the end."""
    for i, line in enumerate(fm_lines):
        if re.match(r"^slug:\s*", line):
            fm_lines = list(fm_lines)
            fm_lines[i] = f'slug: "{new_slug}"'
            return fm_lines
    return fm_lines + [f'slug: "{new_slug}"']


def current_url_slug(folder_name: str, explicit_slug: str | None) -> str:
    """The URL slug Hugo will use before our change."""
    return explicit_slug if explicit_slug else folder_name


def process_post(index_md: Path) -> dict | None:
    text = index_md.read_text(encoding="utf-8")
    fm_lines, body_lines = parse_frontmatter(text)
    title = get_field(fm_lines, "title")
    if not title:
        return {"file": str(index_md), "skipped": "no title"}
    explicit_slug = get_field(fm_lines, "slug")
    folder = index_md.parent.name
    current = current_url_slug(folder, explicit_slug)
    # If the current URL slug is already pure ASCII (letters, digits, -, _),
    # it's a clean English slug. Leave it alone to avoid churning stable URLs.
    if re.fullmatch(r"[A-Za-z0-9\-_]+", current):
        return {"file": str(index_md), "skipped": "already ASCII slug", "slug": current}
    new_slug = slugify(title)
    if not new_slug:
        return {"file": str(index_md), "skipped": "empty generated slug"}
    if new_slug == current:
        return {"file": str(index_md), "skipped": "already clean", "slug": current}

    new_fm = update_slug_line(fm_lines, new_slug)
    old_path = f"/posts/{current}/"
    new_fm = ensure_alias_in_block(new_fm, old_path)

    output = "---\n" + "\n".join(new_fm) + "\n---\n" + "\n".join(body_lines)
    if text.endswith("\n") and not output.endswith("\n"):
        output += "\n"
    index_md.write_text(output, encoding="utf-8")
    return {
        "file": str(index_md.relative_to(BLOG_ROOT)),
        "title": title,
        "old_slug": current,
        "new_slug": new_slug,
        "alias": old_path,
    }


def main() -> int:
    if not EN_POSTS.is_dir():
        print(f"English posts dir not found: {EN_POSTS}", file=sys.stderr)
        return 1
    changed = []
    skipped = []
    for index_md in sorted(EN_POSTS.glob("*/index.md")):
        result = process_post(index_md)
        if result is None:
            continue
        if "skipped" in result:
            skipped.append(result)
        else:
            changed.append(result)

    print(f"Changed: {len(changed)} posts")
    for r in changed:
        print(f"  {r['old_slug']} -> {r['new_slug']}")
    print(f"\nSkipped: {len(skipped)} posts")
    for r in skipped:
        reason = r.get("skipped", "?")
        print(f"  [{reason}] {r['file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
