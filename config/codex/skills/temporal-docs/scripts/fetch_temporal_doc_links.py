#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Extract, normalize, and self-test links from rendered Temporal docs HTML.

Run:
    uv run --script fetch_temporal_doc_links.py /workflows --docs-only --article-only
    uv run --script fetch_temporal_doc_links.py --self-test
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

DOCS_ORIGIN = "https://docs.temporal.io"
STATIC_PREFIXES = (
    "/assets/",
    "/img/",
    "/scripts/",
    "/diagrams/",
)
KNOWN_DOC_URLS = [
    "https://docs.temporal.io/",
    "https://docs.temporal.io/temporal",
    "https://docs.temporal.io/temporal.md",
    "https://docs.temporal.io/workflows",
    "https://docs.temporal.io/workflows.md",
    "https://docs.temporal.io/workflow-definition",
    "https://docs.temporal.io/workflow-definition.md",
    "https://docs.temporal.io/workflow-execution",
    "https://docs.temporal.io/workflow-execution.md",
    "https://docs.temporal.io/workflow-execution/workflowid-runid",
    "https://docs.temporal.io/workflow-execution/event",
    "https://docs.temporal.io/workflow-execution/continue-as-new",
    "https://docs.temporal.io/workflow-execution/limits",
    "https://docs.temporal.io/workflow-execution/timers-delays",
    "https://docs.temporal.io/activities",
    "https://docs.temporal.io/activities.md",
    "https://docs.temporal.io/activity-definition",
    "https://docs.temporal.io/activity-execution",
    "https://docs.temporal.io/activity-operations",
    "https://docs.temporal.io/local-activity",
    "https://docs.temporal.io/standalone-activity",
    "https://docs.temporal.io/encyclopedia/detecting-activity-failures",
    "https://docs.temporal.io/encyclopedia/detecting-application-failures",
    "https://docs.temporal.io/encyclopedia/detecting-application-failures.md",
    "https://docs.temporal.io/encyclopedia/detecting-workflow-failures",
    "https://docs.temporal.io/workers",
    "https://docs.temporal.io/workers.md",
    "https://docs.temporal.io/task-queue",
    "https://docs.temporal.io/tasks",
    "https://docs.temporal.io/develop/worker-performance",
    "https://docs.temporal.io/develop/worker-tuning-reference",
    "https://docs.temporal.io/worker-versioning",
    "https://docs.temporal.io/encyclopedia/event-history/",
    "https://docs.temporal.io/encyclopedia/event-history/event-history-go",
    "https://docs.temporal.io/encyclopedia/event-history/event-history-java",
    "https://docs.temporal.io/encyclopedia/event-history/event-history-python",
    "https://docs.temporal.io/encyclopedia/event-history/event-history-typescript",
    "https://docs.temporal.io/encyclopedia/event-history/event-history-dotnet",
    "https://docs.temporal.io/encyclopedia/workflow-message-passing/",
    "https://docs.temporal.io/sending-messages",
    "https://docs.temporal.io/handling-messages",
    "https://docs.temporal.io/cloud/limits",
    "https://docs.temporal.io/child-workflows",
    "https://docs.temporal.io/child-workflows.md",
    "https://docs.temporal.io/temporal-service",
    "https://docs.temporal.io/temporal-service.md",
    "https://docs.temporal.io/namespaces",
    "https://docs.temporal.io/namespaces.md",
    "https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/event-history/event-history.mdx",
    "https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/workflow-message-passing/workflow-message-passing.mdx",
]
KNOWN_LINK_ASSERTIONS = {
    "https://docs.temporal.io/workflows": {
        "https://docs.temporal.io/workflow-definition",
        "https://docs.temporal.io/workflow-execution",
        "https://docs.temporal.io/schedule",
        "https://docs.temporal.io/dynamic-handler",
        "https://docs.temporal.io/cron-job",
    },
    "https://docs.temporal.io/workflow-execution": {
        "https://docs.temporal.io/workflow-execution/workflowid-runid",
        "https://docs.temporal.io/workflow-execution/event",
        "https://docs.temporal.io/workflow-execution/continue-as-new",
        "https://docs.temporal.io/workflow-execution/limits",
        "https://docs.temporal.io/workflow-execution/timers-delays",
        "https://docs.temporal.io/encyclopedia/event-history/",
    },
    "https://docs.temporal.io/activities": {
        "https://docs.temporal.io/activity-definition",
        "https://docs.temporal.io/activity-execution",
        "https://docs.temporal.io/local-activity",
        "https://docs.temporal.io/standalone-activity",
        "https://docs.temporal.io/workflow-execution/event",
    },
    "https://docs.temporal.io/workers": {
        "https://docs.temporal.io/task-queue",
        "https://docs.temporal.io/tasks",
        "https://docs.temporal.io/temporal-service",
        "https://docs.temporal.io/develop/worker-performance",
        "https://docs.temporal.io/develop/worker-tuning-reference",
    },
    "https://docs.temporal.io/encyclopedia/event-history/": {
        "https://docs.temporal.io/workflow-execution/event",
        "https://docs.temporal.io/encyclopedia/event-history/event-history-go",
        "https://docs.temporal.io/encyclopedia/event-history/event-history-java",
        "https://docs.temporal.io/encyclopedia/event-history/event-history-python",
        "https://docs.temporal.io/encyclopedia/event-history/event-history-typescript",
        "https://docs.temporal.io/encyclopedia/event-history/event-history-dotnet",
    },
    "https://docs.temporal.io/encyclopedia/workflow-message-passing/": {
        "https://docs.temporal.io/sending-messages",
        "https://docs.temporal.io/handling-messages",
        "https://docs.temporal.io/child-workflows",
        "https://docs.temporal.io/cloud/limits",
        "https://docs.temporal.io/workflow-execution/event",
    },
}
KNOWN_FRAGMENT_ASSERTIONS = {
    "https://docs.temporal.io/workflow-execution": {
        "https://docs.temporal.io/workflow-execution/workflowid-runid#workflow-id",
        "https://docs.temporal.io/workflow-execution/workflowid-runid#run-id",
    },
    "https://docs.temporal.io/encyclopedia/workflow-message-passing/": {
        "https://docs.temporal.io/cloud/limits#per-workflow-execution-update-limits",
        "https://docs.temporal.io/workflow-execution/event#event-history",
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
        if tag == "article":
            self.article_depth = 1
        elif self.article_depth:
            self.article_depth += 1

        if tag != "a":
            return
        if self.article_only and not self.article_depth:
            return
        href = dict(attrs).get("href")
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
    if parsed.netloc != "docs.temporal.io":
        return False
    if not docs_only:
        return True
    if any(parsed.path.startswith(prefix) for prefix in STATIC_PREFIXES):
        return False
    if "." in parsed.path.rsplit("/", 1)[-1]:
        return False
    return True


def fetch_html(url: str, timeout: float) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "temporal-docs-skill/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("content-type", "")
        if "text/html" not in content_type:
            raise RuntimeError(f"expected text/html, got {content_type!r}")
        return response.read().decode("utf-8", errors="replace")


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
                "text": re.sub(r"\s+", " ", link["text"]).strip(),
            }
        )
    return results


def strip_fragment(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(parsed._replace(fragment=""))


def check_url(url: str, timeout: float) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "temporal-docs-skill/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        response.read(1)
        return response.headers.get("content-type", "")


def run_self_test(timeout: float) -> int:
    failures: list[str] = []
    for url in KNOWN_DOC_URLS:
        try:
            check_url(url, timeout)
        except Exception as exc:
            failures.append(f"{url}: {exc}")

    for source_url, expected_urls in KNOWN_LINK_ASSERTIONS.items():
        try:
            links = extract_links(
                source_url,
                docs_only=True,
                include_fragments=False,
                article_only=False,
                timeout=timeout,
            )
        except Exception as exc:
            failures.append(f"{source_url}: could not extract links: {exc}")
            continue

        actual_urls = {strip_fragment(link["url"]) for link in links}
        missing = sorted(expected_urls - actual_urls)
        if missing:
            failures.append(f"{source_url}: missing links: {', '.join(missing)}")

    for source_url, expected_urls in KNOWN_FRAGMENT_ASSERTIONS.items():
        try:
            links = extract_links(
                source_url,
                docs_only=True,
                include_fragments=True,
                article_only=True,
                timeout=timeout,
            )
        except Exception as exc:
            failures.append(f"{source_url}: could not extract anchors: {exc}")
            continue

        actual_urls = {link["url"] for link in links}
        missing = sorted(expected_urls - actual_urls)
        if missing:
            failures.append(f"{source_url}: missing anchors: {', '.join(missing)}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print(
        "OK: "
        f"{len(KNOWN_DOC_URLS)} URLs and "
        f"{sum(len(v) for v in KNOWN_LINK_ASSERTIONS.values())} page links and "
        f"{sum(len(v) for v in KNOWN_FRAGMENT_ASSERTIONS.values())} anchors checked"
    )
    return 0


def print_markdown(source_url: str, links: list[dict[str, str]]) -> None:
    print(f"# Links from {source_url}")
    print()
    for link in links:
        label = link["text"] or link["url"]
        print(f"- [{label}]({link['url']})")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="Temporal docs URL or path, such as /workflows",
    )
    parser.add_argument(
        "--docs-only",
        action="store_true",
        help="Keep docs.temporal.io links and filter static assets.",
    )
    parser.add_argument(
        "--include-fragments",
        action="store_true",
        help="Keep URL fragments such as #workflow-id.",
    )
    parser.add_argument(
        "--article-only",
        action="store_true",
        help="Extract links only from the main <article> content.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Check known Temporal docs URLs and expected link relationships.",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)
    if args.self_test:
        return run_self_test(args.timeout)
    if args.url is None:
        print("error: missing url (or use --self-test)", file=sys.stderr)
        return 2

    source_url = normalize_input_url(args.url)
    try:
        links = extract_links(
            source_url,
            args.docs_only,
            args.include_fragments,
            args.article_only,
            args.timeout,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps({"source": source_url, "links": links}, indent=2))
    else:
        print_markdown(source_url, links)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
