#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Build a relevance-ranked index from documentation websites, GitHub trees, or local folders.

Run:
    uv run --script build_docs_index.py https://docs.redpanda.com/streaming/current/home/ --max-pages 60
    uv run --script build_docs_index.py https://github.com/openai/codex/tree/main/sdk/python/docs --top 20
    uv run --script build_docs_index.py ./docs --focus "configuration api" --output /tmp/doc-map.md
    uv run --script build_docs_index.py --self-test
"""

from __future__ import annotations

import argparse
import dataclasses
import html
import json
import posixpath
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

USER_AGENT = "docs-indexer-skill/1.0"

DOC_EXTENSIONS = {
    ".md",
    ".mdx",
    ".rst",
    ".txt",
    ".html",
    ".htm",
}

STATIC_EXTENSIONS = {
    ".7z",
    ".avi",
    ".avif",
    ".bin",
    ".bmp",
    ".css",
    ".csv",
    ".dmg",
    ".doc",
    ".docx",
    ".eot",
    ".exe",
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".mov",
    ".mp3",
    ".mp4",
    ".otf",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".svg",
    ".tar",
    ".tgz",
    ".ttf",
    ".webm",
    ".webp",
    ".woff",
    ".woff2",
    ".xls",
    ".xlsx",
    ".xml",
    ".zip",
}

SKIP_DIRS = {
    ".cache",
    ".git",
    ".hg",
    ".next",
    ".svn",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "site",
    "target",
    "vendor",
}

PRIORITY_TERMS = [
    ("getting started", 34),
    ("quickstart", 34),
    ("quick start", 34),
    ("introduction", 32),
    ("overview", 32),
    ("home", 24),
    ("installation", 24),
    ("install", 24),
    ("setup", 22),
    ("tutorial", 20),
    ("examples", 16),
    ("concepts", 26),
    ("architecture", 26),
    ("design", 18),
    ("internals", 18),
    ("configuration", 24),
    ("configure", 22),
    ("deployment", 20),
    ("operations", 20),
    ("production", 18),
    ("api", 20),
    ("reference", 18),
    ("cli", 16),
    ("sdk", 16),
    ("client", 14),
    ("migration", 20),
    ("upgrade", 18),
    ("troubleshooting", 24),
    ("debugging", 18),
    ("faq", 14),
    ("limits", 18),
    ("best practices", 22),
    ("security", 18),
]

PENALTY_TERMS = [
    "archive",
    "blog",
    "changelog",
    "contributing",
    "cookie",
    "deprecated",
    "events",
    "legal",
    "license",
    "news",
    "privacy",
    "release notes",
    "releases",
    "roadmap",
    "search",
    "terms",
]

CLUSTERS = {
    "Start Here": [
        "getting started",
        "quickstart",
        "quick start",
        "introduction",
        "overview",
        "home",
        "tutorial",
    ],
    "Core Concepts And Architecture": [
        "concepts",
        "architecture",
        "design",
        "internals",
        "model",
        "how it works",
    ],
    "Install, Configure, Operate": [
        "install",
        "installation",
        "setup",
        "configuration",
        "configure",
        "deployment",
        "operations",
        "production",
    ],
    "API And Reference": [
        "api",
        "reference",
        "cli",
        "sdk",
        "client",
        "command",
        "schema",
    ],
    "Troubleshooting, Migration, Limits": [
        "troubleshooting",
        "debugging",
        "faq",
        "migration",
        "upgrade",
        "limits",
        "compatibility",
    ],
}


@dataclass
class Page:
    key: str
    url: str
    source: str
    title: str
    headings: list[str]
    summary: str
    text: str
    raw_links: list[str]
    links: list[str]
    depth: int
    is_seed: bool
    word_count: int
    inbound: int = 0
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)


@dataclass
class CrawlResult:
    pages: dict[str, Page] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


class HtmlDocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.meta_description = ""
        self.headings: list[str] = []
        self.links: list[str] = []
        self.text_parts: list[str] = []
        self._in_title = False
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []
        self._active_href: str | None = None
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {name.lower(): value for name, value in attrs if value is not None}

        if tag in {"script", "style", "svg", "noscript"}:
            self._skip_depth += 1
            return

        if tag == "title":
            self._in_title = True
            return

        if tag == "meta":
            name = attr_map.get("name", "").lower()
            prop = attr_map.get("property", "").lower()
            if name == "description" or prop == "og:description":
                self.meta_description = normalize_space(attr_map.get("content", ""))
            return

        if tag == "a" and attr_map.get("href"):
            self._active_href = html.unescape(attr_map["href"])
            return

        if tag in {"h1", "h2", "h3"}:
            self._heading_tag = tag
            self._heading_parts = []

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_title:
            self.title_parts.append(data)
        if self._heading_tag:
            self._heading_parts.append(data)
        if data.strip():
            self.text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg", "noscript"} and self._skip_depth:
            self._skip_depth -= 1
            return

        if tag == "title":
            self._in_title = False
            return

        if tag == "a" and self._active_href:
            self.links.append(self._active_href)
            self._active_href = None
            return

        if self._heading_tag and tag == self._heading_tag:
            heading = normalize_space(" ".join(self._heading_parts))
            if heading:
                self.headings.append(heading)
            self._heading_tag = None
            self._heading_parts = []


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def strip_markup(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("*", "").replace("_", "")
    return normalize_space(html.unescape(value))


def slug_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower())


def split_focus_terms(raw_focus: list[str]) -> list[str]:
    terms: list[str] = []
    for item in raw_focus:
        for term in re.split(r"[,;]", item):
            normalized = normalize_space(term.lower())
            if normalized:
                terms.append(normalized)
    return terms


def fetch_text(url: str, timeout: float) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("content-type", "")
        raw = response.read()
    return raw.decode("utf-8", errors="replace"), content_type


def parse_html_document(text: str) -> tuple[str, list[str], str, list[str], str]:
    parser = HtmlDocumentParser()
    parser.feed(text)
    title = normalize_space(" ".join(parser.title_parts))
    headings = dedupe_preserve_order(parser.headings)
    if not title and headings:
        title = headings[0]
    body = normalize_space(" ".join(parser.text_parts))
    summary = parser.meta_description or first_paragraph(body)
    return title, headings, summary, parser.links, body


def parse_markdown_document(text: str) -> tuple[str, list[str], str, list[str], str]:
    text_without_frontmatter = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)
    headings = [
        strip_markup(match.group(2))
        for match in re.finditer(r"^(#{1,3})\s+(.+)$", text_without_frontmatter, re.MULTILINE)
    ]
    title = headings[0] if headings else ""
    links = [
        match.group(2).strip()
        for match in re.finditer(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text_without_frontmatter)
    ]
    plain = strip_markup(re.sub(r"```.*?```", " ", text_without_frontmatter, flags=re.DOTALL))
    summary = first_paragraph(text_without_frontmatter)
    return title, dedupe_preserve_order(headings), summary, links, plain


def first_paragraph(text: str) -> str:
    for paragraph in re.split(r"\n\s*\n", text):
        cleaned = strip_markup(paragraph)
        if len(cleaned) >= 30:
            return cleaned[:240]
    cleaned = strip_markup(text)
    return cleaned[:240]


def dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = normalize_space(value)
        key = normalized.lower()
        if normalized and key not in seen:
            seen.add(key)
            result.append(normalized)
    return result


def parse_document(url: str, source: str, text: str, content_type: str, depth: int, is_seed: bool) -> Page:
    lower_url = url.lower()
    lower_content_type = content_type.lower()
    if "html" in lower_content_type or lower_url.endswith((".html", ".htm", "/")):
        title, headings, summary, links, body = parse_html_document(text)
    else:
        title, headings, summary, links, body = parse_markdown_document(text)

    if not title:
        title = title_from_url(url)

    return Page(
        key=url,
        url=url,
        source=source,
        title=title,
        headings=headings[:12],
        summary=summary,
        text=body,
        raw_links=links,
        links=[],
        depth=depth,
        is_seed=is_seed,
        word_count=len(body.split()),
    )


def title_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.rstrip("/")
    name = path.rsplit("/", 1)[-1] if path else parsed.netloc
    if name in {"index.html", "index.md", ""} and "/" in path:
        name = path.rsplit("/", 2)[-2]
    name = re.sub(r"\.(mdx?|rst|html?|txt)$", "", name)
    return normalize_space(name.replace("-", " ").replace("_", " ")).title() or url


def infer_scope_prefix(seed_url: str) -> str:
    parsed = urllib.parse.urlparse(seed_url)
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return "/"

    version_like = re.compile(r"^(v?\d+(?:\.\d+)*|stable|current|latest)$", re.IGNORECASE)
    if version_like.match(parts[0]):
        return f"/{parts[0]}/"

    if len(parts) >= 2 and version_like.match(parts[1]):
        return f"/{parts[0]}/{parts[1]}/"

    if parts[0] in {"docs", "documentation"}:
        return f"/{parts[0]}"

    if len(parts) == 1:
        return f"/{parts[0]}"

    return "/" + "/".join(parts[:-1]) + "/"


def normalize_web_url(base_url: str, href: str) -> str | None:
    href = html.unescape(href).strip()
    if not href or href.startswith(("mailto:", "tel:", "javascript:")):
        return None
    absolute = urllib.parse.urljoin(base_url, href)
    parsed = urllib.parse.urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    parsed = parsed._replace(fragment="", query="")
    path = parsed.path or "/"
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return urllib.parse.urlunparse(parsed._replace(path=path))


def is_probable_doc_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix and suffix in STATIC_EXTENSIONS:
        return False
    lowered = parsed.path.lower()
    if any(part in lowered for part in ["/search", "/assets/", "/static/", "/images/", "/img/", "/css/", "/js/"]):
        return False
    return True


def crawl_web_sources(sources: list[str], args: argparse.Namespace) -> CrawlResult:
    result = CrawlResult()
    allowed_origins = {origin_of(source) for source in sources}
    scope_prefixes: dict[str, list[str]] = defaultdict(list)
    for source in sources:
        origin = origin_of(source)
        prefixes = args.scope_prefix or [infer_scope_prefix(source)]
        scope_prefixes[origin].extend(prefixes)
        result.notes.append(f"web scope {origin}: {', '.join(scope_prefixes[origin])}")

    queue: deque[tuple[str, int]] = deque((normalize_web_url(source, source) or source, 0) for source in sources)
    queued = {url for url, _depth in queue}

    while queue and len(result.pages) < args.max_pages:
        url, depth = queue.popleft()
        if url in result.pages:
            continue
        if depth > args.max_depth:
            continue
        if not is_allowed_web_url(url, allowed_origins, scope_prefixes):
            continue

        try:
            text, content_type = fetch_text(url, args.timeout)
        except Exception as exc:  # noqa: BLE001 - crawl notes should report all fetch failures.
            result.notes.append(f"fetch failed {url}: {exc}")
            continue

        page = parse_document(url=url, source="web", text=text, content_type=content_type, depth=depth, is_seed=depth == 0)
        normalized_links = []
        for href in page.raw_links:
            linked_url = normalize_web_url(url, href)
            if not linked_url:
                continue
            if not is_allowed_web_url(linked_url, allowed_origins, scope_prefixes):
                continue
            normalized_links.append(linked_url)
            if linked_url not in queued and len(queued) < args.max_pages * 4:
                queued.add(linked_url)
                queue.append((linked_url, depth + 1))
        page.links = dedupe_preserve_order(normalized_links)
        result.pages[page.key] = page

    if queue and len(result.pages) >= args.max_pages:
        result.notes.append(f"stopped at --max-pages {args.max_pages}")
    return result


def origin_of(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def is_allowed_web_url(url: str, allowed_origins: set[str], scope_prefixes: dict[str, list[str]]) -> bool:
    parsed = urllib.parse.urlparse(url)
    origin = origin_of(url)
    if origin not in allowed_origins:
        return False
    if not is_probable_doc_url(url):
        return False
    prefixes = scope_prefixes.get(origin) or ["/"]
    return any(parsed.path.startswith(prefix) for prefix in prefixes)


def collect_local_sources(paths: list[Path], args: argparse.Namespace) -> CrawlResult:
    result = CrawlResult()
    for source_path in paths:
        source_path = source_path.expanduser().resolve()
        if not source_path.exists():
            result.notes.append(f"missing local source {source_path}")
            continue

        root = source_path if source_path.is_dir() else source_path.parent
        files = list(iter_doc_files(source_path))[: args.max_pages]
        result.notes.append(f"local source {source_path}: {len(files)} text docs considered")

        key_by_path = {path.resolve(): local_display_url(root, path) for path in files}
        for path in files:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                result.notes.append(f"read failed {path}: {exc}")
                continue
            display_url = key_by_path[path.resolve()]
            page = parse_document(
                url=display_url,
                source="local",
                text=text,
                content_type=content_type_for_path(path),
                depth=local_depth(root, path),
                is_seed=is_local_seed(source_path, root, path),
            )
            page.key = display_url
            page.links = [
                target
                for href in page.raw_links
                if (target := resolve_local_link(path, href, key_by_path)) is not None
            ]
            result.pages[page.key] = page
    return result


def iter_doc_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in DOC_EXTENSIONS else []

    files: list[Path] = []
    for candidate in sorted(path.rglob("*")):
        if not candidate.is_file():
            continue
        if any(part in SKIP_DIRS for part in candidate.parts):
            continue
        if candidate.suffix.lower() in DOC_EXTENSIONS:
            files.append(candidate)
    return files


def local_display_url(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def local_depth(root: Path, path: Path) -> int:
    try:
        return max(0, len(path.resolve().relative_to(root.resolve()).parts) - 1)
    except ValueError:
        return 0


def is_local_seed(source_path: Path, root: Path, path: Path) -> bool:
    if source_path.is_file():
        return path.resolve() == source_path.resolve()
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return len(relative.parts) == 1 and relative.name.lower() in {
        "index.html",
        "index.md",
        "index.mdx",
        "readme.md",
        "readme.mdx",
    }


def content_type_for_path(path: Path) -> str:
    if path.suffix.lower() in {".html", ".htm"}:
        return "text/html"
    return "text/markdown"


def resolve_local_link(base_file: Path, href: str, key_by_path: dict[Path, str]) -> str | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "http://", "https://")):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    candidate = (base_file.parent / urllib.parse.unquote(href)).resolve()
    for resolved in local_candidate_paths(candidate):
        if resolved in key_by_path:
            return key_by_path[resolved]
    return None


def local_candidate_paths(candidate: Path) -> list[Path]:
    candidates = [candidate]
    if candidate.suffix == "":
        candidates.extend(candidate.with_suffix(suffix) for suffix in [".md", ".mdx", ".rst", ".html"])
    if candidate.is_dir() or candidate.suffix == "":
        candidates.extend(candidate / name for name in ["index.md", "index.mdx", "index.rst", "index.html"])
    return [path.resolve() for path in candidates]


def is_github_tree_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.netloc == "github.com" and "/tree/" in parsed.path


def parse_github_tree_url(value: str) -> tuple[str, str, str, str]:
    parsed = urllib.parse.urlparse(value)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 4 or parts[2] != "tree":
        raise ValueError(f"not a GitHub tree URL: {value}")
    owner, repo, _tree, ref, *folder_parts = parts
    return owner, repo, ref, "/".join(folder_parts)


def crawl_github_tree_sources(sources: list[str], args: argparse.Namespace) -> CrawlResult:
    result = CrawlResult()
    for source in sources:
        owner, repo, ref, folder = parse_github_tree_url(source)
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{urllib.parse.quote(ref)}?recursive=1"
        result.notes.append(f"github tree {owner}/{repo}@{ref}:{folder or '.'}")
        try:
            body, _content_type = fetch_text(api_url, args.timeout)
            payload = json.loads(body)
        except Exception as exc:  # noqa: BLE001 - report and keep processing other sources.
            result.notes.append(f"github tree failed {source}: {exc}")
            continue

        if payload.get("truncated"):
            result.notes.append(f"github tree truncated for {owner}/{repo}@{ref}; use a local checkout for completeness")

        entries = [
            item["path"]
            for item in payload.get("tree", [])
            if item.get("type") == "blob"
            and item.get("path", "").startswith(folder)
            and Path(item.get("path", "")).suffix.lower() in DOC_EXTENSIONS
        ][: args.max_pages]
        display_by_path = {
            path: f"https://github.com/{owner}/{repo}/blob/{ref}/{path}"
            for path in entries
        }

        for path in entries:
            raw_url = raw_github_url(owner, repo, ref, path)
            try:
                text, content_type = fetch_text(raw_url, args.timeout)
            except Exception as exc:  # noqa: BLE001 - report all failed docs.
                result.notes.append(f"github raw failed {raw_url}: {exc}")
                continue
            page_url = display_by_path[path]
            page = parse_document(
                url=page_url,
                source="github",
                text=text,
                content_type=content_type_for_path(Path(path)) if not content_type else content_type,
                depth=github_depth(folder, path),
                is_seed=path.endswith(("README.md", "index.md")),
            )
            page.key = page_url
            page.links = [
                target
                for href in page.raw_links
                if (target := resolve_github_link(path, href, display_by_path)) is not None
            ]
            result.pages[page.key] = page
    return result


def raw_github_url(owner: str, repo: str, ref: str, path: str) -> str:
    quoted_path = "/".join(urllib.parse.quote(part) for part in path.split("/"))
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{urllib.parse.quote(ref)}/{quoted_path}"


def github_depth(folder: str, path: str) -> int:
    if not folder:
        return max(0, len(PurePosixPath(path).parts) - 1)
    try:
        relative = PurePosixPath(path).relative_to(PurePosixPath(folder))
    except ValueError:
        return 0
    return max(0, len(relative.parts) - 1)


def resolve_github_link(base_path: str, href: str, display_by_path: dict[str, str]) -> str | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "http://", "https://")):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    normalized = posixpath.normpath(posixpath.join(posixpath.dirname(base_path), urllib.parse.unquote(href)))
    candidates = [normalized]
    if PurePosixPath(normalized).suffix == "":
        candidates.extend(f"{normalized}{suffix}" for suffix in [".md", ".mdx", ".rst", ".html"])
        candidates.extend(f"{normalized}/index{suffix}" for suffix in [".md", ".mdx", ".rst", ".html"])
    for candidate in candidates:
        if candidate in display_by_path:
            return display_by_path[candidate]
    return None


def merge_results(results: list[CrawlResult]) -> CrawlResult:
    merged = CrawlResult()
    for result in results:
        merged.pages.update(result.pages)
        merged.notes.extend(result.notes)
    compute_inbound_counts(merged.pages)
    return merged


def compute_inbound_counts(pages: dict[str, Page]) -> None:
    counts = Counter()
    page_keys = set(pages)
    for page in pages.values():
        for link in page.links:
            if link in page_keys:
                counts[link] += 1
    for key, page in pages.items():
        page.inbound = counts[key]


def score_pages(pages: dict[str, Page], focus_terms: list[str]) -> list[Page]:
    for page in pages.values():
        score, reasons = score_page(page, focus_terms)
        page.score = score
        page.reasons = reasons
    return sorted(pages.values(), key=lambda item: (-item.score, item.depth, item.url))


def score_page(page: Page, focus_terms: list[str]) -> tuple[float, list[str]]:
    title_path = slug_text(f"{page.title} {page.url}")
    headings = slug_text(" ".join(page.headings[:6]))
    text = slug_text(page.text[:6000])
    reasons: list[str] = []

    score = 0.0
    if page.is_seed:
        score += 70
        reasons.append("seed page")
    if page.depth <= 1:
        score += 16 - (page.depth * 6)
        reasons.append(f"depth {page.depth}")
    else:
        score += max(0, 8 - page.depth)

    if page.inbound:
        score += min(28, page.inbound * 4)
        reasons.append(f"{page.inbound} inbound links")

    matched_priority: list[str] = []
    for term, weight in PRIORITY_TERMS:
        term_slug = slug_text(term)
        if term_slug in title_path:
            score += weight
            matched_priority.append(term)
        elif term_slug in headings:
            score += weight * 0.55
            matched_priority.append(term)
    if matched_priority:
        reasons.append("matches " + ", ".join(dedupe_preserve_order(matched_priority[:3])))

    focus_matches: list[str] = []
    for term in focus_terms:
        term_slug = slug_text(term)
        if not term_slug:
            continue
        if term_slug in title_path:
            score += 38
            focus_matches.append(term)
        elif term_slug in headings:
            score += 22
            focus_matches.append(term)
        elif term_slug in text:
            score += 8
            focus_matches.append(term)
    if focus_matches:
        reasons.append("focus " + ", ".join(dedupe_preserve_order(focus_matches[:3])))

    penalties = [term for term in PENALTY_TERMS if slug_text(term) in title_path]
    if penalties and not focus_terms:
        score -= 24
        reasons.append("lower priority " + ", ".join(penalties[:2]))

    if page.word_count < 80:
        score -= 10
        reasons.append("short page")

    if not reasons:
        reasons.append("nearby documentation page")
    return round(score, 1), reasons[:4]


def render_markdown(pages: list[Page], notes: list[str], args: argparse.Namespace) -> str:
    top_pages = pages[: args.top]
    lines = [
        "# Documentation Index",
        "",
        f"Sources: {', '.join(args.sources)}",
        f"Pages indexed: {len(pages)}",
        f"Focus: {', '.join(split_focus_terms(args.focus)) or 'general documentation importance'}",
        "",
        "## Top Pages",
        "",
        "| Rank | Score | Page | Why |",
        "|---:|---:|---|---|",
    ]
    for rank, page in enumerate(top_pages, start=1):
        lines.append(
            f"| {rank} | {page.score:g} | {format_page_link(page)} | {escape_table_text('; '.join(page.reasons))} |"
        )

    lines.extend(["", "## Suggested Doc Map", ""])
    for cluster, terms in CLUSTERS.items():
        cluster_pages = [page for page in pages if page_matches_cluster(page, cluster, terms)][:5]
        if not cluster_pages:
            continue
        lines.extend([f"### {cluster}", ""])
        for page in cluster_pages:
            lines.append(f"- {format_page_link(page)} - {', '.join(page.reasons[:2])}")
        lines.append("")

    lines.extend(["## Crawl Notes", ""])
    if notes:
        for note in notes:
            lines.append(f"- {note}")
    else:
        lines.append("- No crawl notes.")
    lines.append("")
    return "\n".join(lines)


def render_json(pages: list[Page], notes: list[str], args: argparse.Namespace) -> str:
    payload = {
        "sources": args.sources,
        "focus": split_focus_terms(args.focus),
        "page_count": len(pages),
        "notes": notes,
        "pages": [page_to_json(page) for page in pages[: args.top]],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def page_to_json(page: Page) -> dict[str, object]:
    return {
        "url": page.url,
        "source": page.source,
        "title": page.title,
        "score": page.score,
        "reasons": page.reasons,
        "summary": page.summary,
        "headings": page.headings[:8],
        "inbound": page.inbound,
        "depth": page.depth,
        "word_count": page.word_count,
    }


def format_page_link(page: Page) -> str:
    label = escape_table_text(page.title or page.url)
    if page.url.startswith(("http://", "https://")):
        return f"[{label}]({page.url})"
    return f"[{label}](<{page.url}>)"


def escape_table_text(value: str) -> str:
    return normalize_space(value).replace("|", "\\|")


def page_matches_cluster(page: Page, cluster: str, terms: list[str]) -> bool:
    if cluster == "Start Here" and page.is_seed:
        return True
    haystack = slug_text(f"{page.title} {page.url} {' '.join(page.headings[:6])}")
    return any(slug_text(term) in haystack for term in terms)


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "index.md").write_text(
            """# ExampleDB Documentation

Welcome to ExampleDB.

- [Quickstart](quickstart.md)
- [Architecture](concepts/architecture.md)
- [API Reference](reference/api.md)
- [Release Notes](release-notes.md)
""",
            encoding="utf-8",
        )
        (root / "quickstart.md").write_text(
            """# Quickstart

Install ExampleDB and run your first query.
""",
            encoding="utf-8",
        )
        (root / "concepts").mkdir()
        (root / "concepts" / "architecture.md").write_text(
            """# Architecture

ExampleDB stores data in partitions and replicates them across nodes.
""",
            encoding="utf-8",
        )
        (root / "reference").mkdir()
        (root / "reference" / "api.md").write_text(
            """# API Reference

Client SDK and CLI reference.
""",
            encoding="utf-8",
        )
        (root / "release-notes.md").write_text("# Release Notes\n\nOld changes.\n", encoding="utf-8")

        args = parse_args([str(root), "--focus", "architecture", "--top", "4"])
        result = collect_local_sources([root], args)
        compute_inbound_counts(result.pages)
        pages = score_pages(result.pages, split_focus_terms(args.focus))
        output = render_markdown(pages, result.notes, args)

        top_urls = [page.url for page in pages[:3]]
        if not any("architecture.md" in url for url in top_urls):
            print("FAIL architecture focus did not rank architecture page near the top", file=sys.stderr)
            print(output, file=sys.stderr)
            return 1
        if "## Suggested Doc Map" not in output:
            print("FAIL markdown output missing suggested doc map", file=sys.stderr)
            return 1
        print("self-test passed")
        return 0


def partition_sources(sources: list[str]) -> tuple[list[str], list[str], list[Path]]:
    web_sources: list[str] = []
    github_sources: list[str] = []
    local_sources: list[Path] = []
    for source in sources:
        if is_github_tree_url(source):
            github_sources.append(source)
        elif source.startswith(("http://", "https://")):
            web_sources.append(source)
        else:
            local_sources.append(Path(source))
    return web_sources, github_sources, local_sources


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="*", help="Documentation website URL, GitHub tree URL, or local docs path")
    parser.add_argument("--focus", action="append", default=[], help="Topic terms to prioritize; repeat or comma-separate")
    parser.add_argument("--scope-prefix", action="append", help="Website path prefix to keep, such as /docs or /streaming/current/")
    parser.add_argument("--max-pages", type=int, default=80, help="Maximum pages/files per source class to index")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum link depth for website crawls")
    parser.add_argument("--top", type=int, default=25, help="Number of ranked pages to emit")
    parser.add_argument("--timeout", type=float, default=12.0, help="Network timeout in seconds")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    parser.add_argument("--output", help="Write output to this file instead of stdout")
    parser.add_argument("--self-test", action="store_true", help="Run a no-network self-test")
    args = parser.parse_args(argv)
    if not args.self_test and not args.sources:
        parser.error("provide at least one source or --self-test")
    if args.max_pages < 1:
        parser.error("--max-pages must be positive")
    if args.max_depth < 0:
        parser.error("--max-depth must be non-negative")
    if args.top < 1:
        parser.error("--top must be positive")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        return run_self_test()

    web_sources, github_sources, local_sources = partition_sources(args.sources)
    results: list[CrawlResult] = []
    if web_sources:
        results.append(crawl_web_sources(web_sources, args))
    if github_sources:
        results.append(crawl_github_tree_sources(github_sources, args))
    if local_sources:
        results.append(collect_local_sources(local_sources, args))

    merged = merge_results(results)
    ranked_pages = score_pages(merged.pages, split_focus_terms(args.focus))
    output = render_json(ranked_pages, merged.notes, args) if args.format == "json" else render_markdown(ranked_pages, merged.notes, args)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
