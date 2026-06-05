# Docs Indexer Source Strategy

Use this reference when choosing how to crawl a documentation source and how tightly to bound it.

## Source Priority

1. Use local docs folders when the repository is already checked out. This avoids auth, rate limits, and rendered-site navigation noise.
2. Use GitHub tree URLs for public docs folders when a checkout is not available.
3. Use rendered documentation websites when the public site is the source of truth or when sidebar/body links matter.
4. Use `llms.txt`, sitemap XML, sidebar manifests, or repository TOCs as supplemental seeds when a site exposes them, but still read final pages before making claims.

## Website Crawls

Start from the canonical docs entry page and keep the crawl inside one docs scope:

```sh
uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py \
  https://kafka.apache.org/43/getting-started/introduction/ \
  --scope-prefix /43/ \
  --max-pages 80
```

Use `--scope-prefix` when the site has shared marketing, blog, API, or version-switcher links. Good prefixes usually include the docs version or product section:

- Kafka 4.3 docs: `/43/`
- Redpanda current streaming docs: `/streaming/current/`
- Debezium stable reference: `/documentation/reference/stable/`
- Dragonfly docs: `/docs`

Raise `--max-depth` only after checking whether the crawl notes show relevant pages were skipped by depth. Prefer a tighter scope over a larger crawl.

## GitHub Tree Crawls

For public GitHub docs folders, pass the tree URL directly:

```sh
uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py \
  https://github.com/openai/codex/tree/main/sdk/python/docs
```

The helper reads the repository tree through the public GitHub API, filters text documentation files under the requested folder, and fetches raw content. It assumes the first path segment after `/tree/` is the ref. If a branch name contains slashes or the repo is private, use a local checkout.

## Local Folder Crawls

Use local mode for private repos, generated docs, vendored docs, or source trees already on disk:

```sh
uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py ./docs --top 40
```

The helper recursively reads Markdown, MDX, reStructuredText, text, and HTML files. It skips common generated and dependency folders such as `.git`, `node_modules`, `dist`, `build`, `target`, and `__pycache__`.

## Failure Modes

- If the top pages are mostly nav, release notes, or unrelated marketing pages, rerun with `--scope-prefix`.
- If a JavaScript-rendered site exposes few links, look for a sitemap, `llms.txt`, source repo, or local checkout and use that as the source.
- If the crawl returns too many reference pages, add `--focus` terms or lower `--top`.
- If the website blocks automated requests, stop and use a local clone, official sitemap, or manual page list. Do not add secrets or bypass controls.
