#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "diskcache>=5.6,<6",
#   "httpx>=0.27,<1",
#   "rich>=13,<15",
#   "tenacity>=8.2,<10",
# ]
# ///
"""Gold-standard HTTP fetcher with timeouts, retries, cache, and demo mode.

Run:
    uv run --script fetch_http.py --demo
    uv run --script fetch_http.py https://example.com --output example.html
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import diskcache
import httpx
from rich.console import Console
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

console = Console()
error_console = Console(stderr=True)


class HttpClient(Protocol):
    def get(
        self, url: str, *, headers: dict[str, str], timeout: float
    ) -> httpx.Response: ...


@dataclass(frozen=True)
class FetchResult:
    url: str
    status_code: int
    content_type: str
    body: bytes
    from_cache: bool


def cache_key(url: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return f"fetch:{digest}"


def guess_output_path(url: str, content_type: str, output_dir: Path) -> Path:
    suffix = ".json" if "json" in content_type else ".html"
    stem = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    return output_dir / f"response-{stem}{suffix}"


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


@retry(
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.TransportError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.25, max=2.0),
    reraise=True,
)
def fetch_uncached(client: HttpClient, url: str, timeout: float) -> httpx.Response:
    return client.get(
        url, headers={"user-agent": "uv-scripts-fetch-http/1.0"}, timeout=timeout
    )


def fetch_url(
    client: HttpClient,
    url: str,
    *,
    timeout: float,
    cache_dir: Path,
    refresh: bool,
) -> FetchResult:
    key = cache_key(url)
    with diskcache.Cache(cache_dir) as cache:
        if not refresh and key in cache:
            cached = cache[key]
            return FetchResult(
                url=url,
                status_code=cached["status_code"],
                content_type=cached["content_type"],
                body=cached["body"],
                from_cache=True,
            )

        response = fetch_uncached(client, url, timeout)
        response.raise_for_status()
        result = FetchResult(
            url=url,
            status_code=response.status_code,
            content_type=response.headers.get("content-type", ""),
            body=response.content,
            from_cache=False,
        )
        cache[key] = {
            "status_code": result.status_code,
            "content_type": result.content_type,
            "body": result.body,
        }
        return result


def make_demo_client() -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = {"ok": True, "url": str(request.url), "items": ["alpha", "beta"]}
        return httpx.Response(
            200, json=payload, headers={"content-type": "application/json"}
        )

    return httpx.Client(transport=httpx.MockTransport(handler))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a URL with retries, cache, and safe output."
    )
    parser.add_argument("url", nargs="?", help="URL to fetch.")
    parser.add_argument(
        "--output", type=Path, help="Output file. Defaults to a hashed file name."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory for default output.",
    )
    parser.add_argument(
        "--cache-dir", type=Path, default=Path(".uv-script-cache/fetch-http")
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument(
        "--refresh", action="store_true", help="Ignore cached response."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run without network using a mock HTTP client.",
    )
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    url = args.url or "https://example.invalid/api/demo"
    if not args.demo and args.url is None:
        error_console.print("[red]missing url[/red] (or use --demo)")
        return 2

    client: HttpClient
    if args.demo:
        client_context = make_demo_client()
    else:
        client_context = httpx.Client(follow_redirects=True)

    with client_context as client:
        result = fetch_url(
            client,
            url,
            timeout=args.timeout,
            cache_dir=args.cache_dir,
            refresh=args.refresh,
        )

    output = args.output or guess_output_path(
        result.url, result.content_type, args.output_dir
    )
    atomic_write(output, result.body)

    console.print(f"[green]saved[/green] {output}")
    console.print(
        f"status={result.status_code} content_type={result.content_type or 'unknown'}"
    )
    console.print(f"cache={'hit' if result.from_cache else 'miss'}")

    if "json" in result.content_type:
        preview = json.loads(result.body)
        console.print_json(json.dumps(preview))

    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except httpx.HTTPStatusError as exc:
        error_console.print(
            f"[red]http error[/red] {exc.response.status_code}: {exc.request.url}"
        )
        return 1
    except httpx.HTTPError as exc:
        error_console.print(f"[red]http failure[/red] {exc}")
        return 1
    except KeyboardInterrupt:
        error_console.print("[red]interrupted[/red]")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
