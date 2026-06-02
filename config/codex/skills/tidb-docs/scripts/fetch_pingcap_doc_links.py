#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Extract, normalize, and self-test links from rendered PingCAP docs HTML.

Run:
    uv run --script fetch_pingcap_doc_links.py /tidb/stable/overview/ --docs-only
    uv run --script fetch_pingcap_doc_links.py --self-test
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

DOCS_ORIGIN = "https://docs.pingcap.com"
USER_AGENT = "tidb-docs-skill/1.0"
STATIC_PREFIXES = (
    "/media/",
    "/assets/",
    "/images/",
    "/img/",
    "/scripts/",
    "/_next/",
)

KNOWN_DOC_URLS = [
    "https://docs.pingcap.com/llms.txt",
    "https://docs.pingcap.com/tidb/llms.txt",
    "https://docs.pingcap.com/developer/llms.txt",
    "https://docs.pingcap.com/best-practices/llms.txt",
    "https://docs.pingcap.com/ai/llms.txt",
    "https://docs.pingcap.com/api/llms.txt",
    "https://docs.pingcap.com/tidb/stable/",
    "https://docs.pingcap.com/tidb/stable/overview.md",
    "https://docs.pingcap.com/tidb/stable/mysql-compatibility.md",
    "https://docs.pingcap.com/tidb/stable/tidb-limitations.md",
    "https://docs.pingcap.com/tidb/stable/tidb-architecture.md",
    "https://docs.pingcap.com/tidb/stable/tidb-storage.md",
    "https://docs.pingcap.com/tidb/stable/tidb-computing.md",
    "https://docs.pingcap.com/tidb/stable/tidb-scheduling.md",
    "https://docs.pingcap.com/tidb/stable/quick-start-with-tidb.md",
    "https://docs.pingcap.com/tidb/stable/tiup-playground.md",
    "https://docs.pingcap.com/tidb/stable/hardware-and-software-requirements.md",
    "https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup.md",
    "https://docs.pingcap.com/tidb/stable/ticdc-overview.md",
    "https://docs.pingcap.com/tidb/stable/dm-overview.md",
    "https://docs.pingcap.com/tidb/stable/tidb-lightning-overview.md",
    "https://docs.pingcap.com/tidb/stable/performance-tuning-overview.md",
    "https://docs.pingcap.com/tidb/stable/explain-overview.md",
    "https://docs.pingcap.com/tidb/stable/system-variables.md",
    "https://docs.pingcap.com/tidb/stable/information-schema.md",
    "https://docs.pingcap.com/developer/dev-guide-connect-to-tidb.md",
    "https://docs.pingcap.com/best-practices/tidb-best-practices.md",
    "https://docs.pingcap.com/ai/vector-search-overview.md",
]

KNOWN_LINK_ASSERTIONS = {
    "https://docs.pingcap.com/tidb/stable/overview/": {
        "https://docs.pingcap.com/tidb/stable/tidb-architecture/",
        "https://docs.pingcap.com/tidb/stable/tidb-storage/",
        "https://docs.pingcap.com/tidb/stable/tidb-computing/",
        "https://docs.pingcap.com/tidb/stable/tidb-scheduling/",
    },
    "https://docs.pingcap.com/tidb/stable/": {
        "https://docs.pingcap.com/tidb/stable/hardware-and-software-requirements/",
        "https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup/",
        "https://docs.pingcap.com/tidb/stable/maintain-tidb-using-tiup/",
        "https://docs.pingcap.com/tidb/stable/tiup-overview/",
        "https://docs.pingcap.com/tidb/stable/system-variables/",
    },
    "https://docs.pingcap.com/ai/": {
        "https://docs.pingcap.com/ai/vector-search-overview/",
        "https://docs.pingcap.com/ai/vector-search/",
        "https://docs.pingcap.com/ai/vector-search-hybrid-search/",
        "https://docs.pingcap.com/ai/vector-search-data-types/",
    },
}


class AnchorParser(HTMLParser):
    def __init__(self, article_only: bool) -> None:
        super().__init__(convert_charrefs=True)
        self.article_only = article_only
        self.article_depth = 0
        self.links: list[dict[str, str]] = []
        self._active_href: str | None = None
        self._active_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "article" or attr_map.get("role") == "main":
            self.article_depth = 1
        elif self.article_depth:
            self.article_depth += 1

        if tag != "a":
            return
        if self.article_only and not self.article_depth:
            return
        href = attr_map.get("href")
        if href:
            self._active_href = href
            self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_href:
            self._active_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._active_href:
            text = " ".join("".join(self._active_text).split())
            self.links.append({"href": self._active_href, "text": text})
            self._active_href = None
            self._active_text = []

        if self.article_depth:
            self.article_depth -= 1


def normalize_input_url(value: str) -> str:
    if value.startswith(("http://", "https://")):
        return value
    if not value.startswith("/"):
        value = "/" + value
    return urllib.parse.urljoin(DOCS_ORIGIN, value)


def strip_fragment(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(parsed._replace(fragment=""))


def canonicalize_for_match(url: str) -> str:
    parsed = urllib.parse.urlparse(strip_fragment(url))
    path = re.sub(r"^/tidb/v\d+\.\d+/", "/tidb/stable/", parsed.path)
    if path.endswith(".md"):
        path = path[:-3] + "/"
    elif path and not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    return urllib.parse.urlunparse(parsed._replace(path=path))


def normalize_href(base_url: str, href: str, include_fragments: bool) -> str | None:
    href = href.strip()
    if not href or href.startswith(("mailto:", "tel:", "javascript:")):
        return None

    absolute = urllib.parse.urljoin(base_url, html.unescape(href))
    parsed = urllib.parse.urlparse(absolute)
    if not include_fragments:
        parsed = parsed._replace(fragment="")
    return urllib.parse.urlunparse(parsed)


def is_docs_link(url: str, docs_only: bool) -> bool:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "docs.pingcap.com":
        return False
    if not docs_only:
        return True
    if any(parsed.path.startswith(prefix) for prefix in STATIC_PREFIXES):
        return False
    return True


def fetch_text(url: str, timeout: float) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("content-type", "")
        body = response.read().decode("utf-8", errors="replace")
    return body, content_type


def fetch_html(url: str, timeout: float) -> str:
    body, content_type = fetch_text(url, timeout)
    if "text/html" not in content_type:
        raise RuntimeError(f"expected text/html, got {content_type!r}")
    return body


def extract_links(
    url: str,
    docs_only: bool,
    include_fragments: bool,
    article_only: bool,
    timeout: float,
) -> list[dict[str, str]]:
    parser = AnchorParser(article_only=article_only)
    parser.feed(fetch_html(url, timeout))

    seen: set[str] = set()
    results: list[dict[str, str]] = []
    for link in parser.links:
        normalized = normalize_href(url, link["href"], include_fragments)
        if not normalized or not is_docs_link(normalized, docs_only):
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        results.append(
            {
                "url": normalized,
                "canonical_url": canonicalize_for_match(normalized),
                "text": re.sub(r"\s+", " ", link["text"]).strip(),
            }
        )
    return results


def check_url(url: str, timeout: float) -> str:
    _, content_type = fetch_text(url, timeout)
    return content_type


def run_self_test(timeout: float) -> int:
    failures: list[str] = []

    for url in KNOWN_DOC_URLS:
        try:
            content_type = check_url(url, timeout)
            print(f"ok url {url} [{content_type}]")
        except Exception as exc:  # noqa: BLE001 - self-test should report all failures.
            failures.append(f"url failed {url}: {exc}")

    for source, expected_links in KNOWN_LINK_ASSERTIONS.items():
        try:
            links = extract_links(
                source,
                docs_only=True,
                include_fragments=False,
                article_only=False,
                timeout=timeout,
            )
        except Exception as exc:  # noqa: BLE001 - self-test should report all failures.
            failures.append(f"extract failed {source}: {exc}")
            continue

        actual = {item["canonical_url"] for item in links}
        expected = {canonicalize_for_match(url) for url in expected_links}
        missing = sorted(expected - actual)
        if missing:
            failures.append(f"missing links from {source}: {', '.join(missing)}")
        else:
            print(f"ok links {source} ({len(expected)} assertions)")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    print("self-test passed")
    return 0


def format_markdown(url: str, links: list[dict[str, str]]) -> str:
    lines = [f"# Links from {url}", ""]
    for link in links:
        label = link["text"] or link["url"]
        lines.append(f"- [{label}]({link['url']})")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract links from rendered PingCAP docs pages.",
    )
    parser.add_argument("url", nargs="?", help="Docs URL or path to inspect")
    parser.add_argument("--docs-only", action="store_true", help="Keep docs.pingcap.com links only")
    parser.add_argument("--article-only", action="store_true", help="Keep links in article/main content only")
    parser.add_argument("--include-fragments", action="store_true", help="Preserve URL fragments")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--self-test", action="store_true", help="Check known docs URLs and link assertions")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test(args.timeout)

    if not args.url:
        parser.error("url is required unless --self-test is used")

    url = normalize_input_url(args.url)
    links = extract_links(
        url,
        docs_only=args.docs_only,
        include_fragments=args.include_fragments,
        article_only=args.article_only,
        timeout=args.timeout,
    )

    if args.format == "json":
        print(json.dumps({"source": url, "links": links}, indent=2))
    else:
        print(format_markdown(url, links))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
