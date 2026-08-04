#!/usr/bin/env python3
"""Download CJK web fonts for self-hosting.

Downloads:
  - Noto Sans TC (Google Fonts, ~105 woff2 segments)
  - LXGW WenKai TC (jsDelivr/npm, 6 font families, ~130 woff2 each)

Output directory: fonts/
"""

import argparse
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
})

GOOGLE_FONTS_CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Noto+Sans+TC:wght@100..900&display=swap"
)

LXGW_BASE = "https://cdn.jsdelivr.net/npm/lxgw-wenkai-tc-web@1.522.0"
LXGW_FAMILIES = [
    "lxgwwenkaimonotc-light",
    "lxgwwenkaimonotc-medium",
    "lxgwwenkaimonotc-regular",
    "lxgwwenkaitc-light",
    "lxgwwenkaitc-medium",
    "lxgwwenkaitc-regular",
]

WOFF2_RE = re.compile(r"""url\(['"]?(https://fonts\.gstatic\.com/s/[^)'"]+\.woff2)['"]?\)""")
LXGW_FILE_RE = re.compile(r"\d+\.woff2")


def download_file(url: str, dest: Path, label: str = "") -> None:
    """Download a single file with progress tracking."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    resp = SESSION.get(url, stream=True, timeout=120)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    written = 0
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
            written += len(chunk)
    status = "OK" if written == total else f"PARTIAL ({written}/{total})"
    print(f"  [{status}] {label or dest.name}")


def download_noto_sans_tc(out_dir: Path, max_workers: int) -> None:
    """Download all Noto Sans TC woff2 segments from Google Fonts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Fetching Google Fonts CSS ...")
    resp = SESSION.get(GOOGLE_FONTS_CSS_URL, timeout=30)
    resp.raise_for_status()
    css = resp.text

    urls = WOFF2_RE.findall(css)
    print(f"Found {len(urls)} woff2 segments for Noto Sans TC")

    tasks = []
    for url in urls:
        fname = url.split("/")[-1]
        dest = out_dir / fname
        if dest.exists():
            continue
        tasks.append((url, dest, fname))

    if not tasks:
        print("  All Noto Sans TC files already downloaded.")
        return

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(download_file, url, dest, label): label
            for url, dest, label in tasks
        }
        for fut in as_completed(futures):
            try:
                fut.result()
            except Exception as e:
                print(f"  [FAIL] {futures[fut]}: {e}")

    print(f"Done. Files in {out_dir}/")


def count_woff2_in_dir(directory: str) -> int:
    """HTTP HEAD to find how many woff2 files a family has."""
    count = 0
    for i in range(300):
        url = f"{LXGW_BASE}/{directory}/{i}.woff2"
        resp = SESSION.head(url, timeout=10, allow_redirects=True)
        if resp.status_code == 200:
            count += 1
        else:
            break
    return count


def download_lxgw_family(family: str, out_dir: Path, max_workers: int) -> None:
    """Download all woff2 files for one LXGW font family."""
    family_dir = out_dir / family
    family_dir.mkdir(parents=True, exist_ok=True)

    # Determine how many segments
    css_url = f"{LXGW_BASE}/{family}/result.css"
    resp = SESSION.get(css_url, timeout=30)
    resp.raise_for_status()
    css = resp.text

    # Find max segment index from the CSS
    indices = set()
    for m in re.finditer(r"(\d+)\.woff2", css):
        indices.add(int(m.group(1)))

    if not indices:
        print(f"  Could not parse segments for {family}, skipping.")
        return

    max_idx = max(indices)
    print(f"  {family}: {max_idx + 1} segments")

    tasks = []
    for i in range(max_idx + 1):
        url = f"{LXGW_BASE}/{family}/{i}.woff2"
        dest = family_dir / f"{i}.woff2"
        if dest.exists():
            continue
        tasks.append((url, dest, f"{family}/{i}.woff2"))

    if not tasks:
        print(f"  All files for {family} already downloaded.")
        return

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(download_file, url, dest, label): label
            for url, dest, label in tasks
        }
        for fut in as_completed(futures):
            try:
                fut.result()
            except Exception as e:
                print(f"  [FAIL] {futures[fut]}: {e}")

    # Also download the CSS for reference
    css_dest = family_dir / "result.css"
    if not css_dest.exists():
        css_dest.write_text(css)
        print(f"  Saved {family}/result.css")


def download_lxgw(out_dir: Path, families: list[str], max_workers: int) -> None:
    """Download all specified LXGW font families."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for family in families:
        print(f"Downloading LXGW: {family}")
        download_lxgw_family(family, out_dir, max_workers)
    print(f"Done. Files in {out_dir}/")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download CJK web fonts for self-hosting")
    parser.add_argument(
        "-o", "--output", default="fonts",
        help="Output directory (default: fonts)",
    )
    parser.add_argument(
        "-j", "--jobs", type=int, default=16,
        help="Max concurrent downloads (default: 16)",
    )
    parser.add_argument(
        "--noto-only", action="store_true",
        help="Only download Noto Sans TC",
    )
    parser.add_argument(
        "--lxgw-only", action="store_true",
        help="Only download LXGW WenKai TC",
    )
    parser.add_argument(
        "--lxgw-families", nargs="+", default=LXGW_FAMILIES,
        help=f"LXGW families to download (default: all {len(LXGW_FAMILIES)})",
    )
    args = parser.parse_args()

    base = Path(args.output)

    if not args.lxgw_only:
        print("=== Noto Sans TC ===")
        download_noto_sans_tc(base / "noto-sans-tc", args.jobs)
        print()

    if not args.noto_only:
        print("=== LXGW WenKai TC ===")
        download_lxgw(base, args.lxgw_families, args.jobs)
        print()

    # Summary
    total = sum(1 for _ in base.rglob("*.woff2"))
    size = sum(f.stat().st_size for f in base.rglob("*.woff2"))
    print(f"Total: {total} woff2 files, {size / 1024 / 1024:.1f} MB")
    print("\nNext steps:")
    print("  1. Upload fonts/ to your Cloudflare R2 bucket")
    print("  2. Update your VuePress config to point to the new URLs")


if __name__ == "__main__":
    main()
