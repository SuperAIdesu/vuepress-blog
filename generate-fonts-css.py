#!/usr/bin/env python3
"""Generate self-hosted @font-face CSS from downloaded font files.

Reads local font CSS (result.css) and Google Fonts CSS, rewrites src URLs
to point to the Cloudflare R2 bucket, and outputs a single CSS file.
"""

import re
import requests
from pathlib import Path

BUCKET = "https://public-oss.sbeam.dev/webfonts"

GOOGLE_FONTS_CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Noto+Sans+TC:wght@100..900&display=swap"
)

LXGW_FAMILIES = [
    ("lxgwwenkaitc-regular", "LXGW WenKai TC"),
    ("lxgwwenkaimonotc-regular", "LXGW WenKai Mono TC"),
]

FONT_DIR = Path("fonts")
OUTPUT = Path("src/.vuepress/styles/fonts.css")


def generate_noto_css() -> str:
    """Fetch Google Fonts CSS and rewrite URLs to our bucket."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
    })
    resp = session.get(GOOGLE_FONTS_CSS_URL, timeout=30)
    resp.raise_for_status()
    css = resp.text

    def rewrite_url(m: re.Match) -> str:
        full = m.group(1)
        filename = full.split("/")[-1]
        return f"url('{BUCKET}/noto-sans-tc/{filename}')"

    css = re.sub(
        r"url\(([^)]+)\)",
        rewrite_url,
        css,
    )
    return css


def generate_lxgw_css(family_dir: str) -> str:
    """Read local result.css and rewrite URLs to our bucket."""
    css_path = FONT_DIR / family_dir / "result.css"
    css = css_path.read_text(encoding="utf-8")

    def rewrite_url(m: re.Match) -> str:
        filename = m.group(1)
        return f"url('{BUCKET}/{family_dir}/{filename}')"

    css = re.sub(
        r'url\("./([^"]+\.woff2)"\)',
        rewrite_url,
        css,
    )
    return css


def main() -> None:
    parts = []

    # Noto Sans TC
    print("Generating Noto Sans TC ...")
    parts.append(generate_noto_css())

    # LXGW families
    for family_dir, _ in LXGW_FAMILIES:
        print(f"Generating {family_dir} ...")
        parts.append(generate_lxgw_css(family_dir))

    output = "\n".join(parts)
    OUTPUT.write_text(output, encoding="utf-8")
    size = OUTPUT.stat().st_size
    print(f"Written to {OUTPUT} ({size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
