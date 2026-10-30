# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Search the Rex docs and print the best-matching sections."""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request

SEARCH_URL = "https://www.superlogical.com/rex/docs/search.json"


def page_url(section_url: str) -> str:
    base = section_url.split("#", 1)[0]
    return base if base.endswith(".md") else f"{base}.md"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="words to search for")
    parser.add_argument("-n", "--limit", type=int, default=5, help="sections to show (max 10)")
    args = parser.parse_args()

    url = f"{SEARCH_URL}?{urllib.parse.urlencode({'q': args.query})}"
    with urllib.request.urlopen(url, timeout=15) as response:
        hits = json.load(response)

    for hit in hits[: args.limit]:
        heading = hit.get("heading") or hit.get("page") or ""
        text = " ".join(hit.get("text", "").split())
        print(f"{hit['url']}  [{heading}]")
        print(f"  page: {page_url(hit['url'])}")
        print(f"  {text[:280]}")


if __name__ == "__main__":
    main()
