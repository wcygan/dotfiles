# TiDB Docs Source Model

Checked: 2026-06-02

Use this reference when URL shape, source freshness, or page adjacency matters.

## Source Priority

1. Fetch live official docs from `https://docs.pingcap.com/`.
2. Use product `llms.txt` files as fast indexes with page summaries.
3. Use rendered HTML when sidebar, page-body links, anchors, or page relationships matter.
4. Use the `pingcap/docs` repository TOC files for broad navigation and source structure.
5. Use raw repository Markdown only when a rendered docs page or `.md` endpoint is unavailable.

## Official Indexes

- Global product index: `https://docs.pingcap.com/llms.txt`
- TiDB Self-Managed index: `https://docs.pingcap.com/tidb/llms.txt`
- Developer Guide index: `https://docs.pingcap.com/developer/llms.txt`
- Best Practices index: `https://docs.pingcap.com/best-practices/llms.txt`
- TiDB for AI index: `https://docs.pingcap.com/ai/llms.txt`
- API index: `https://docs.pingcap.com/api/llms.txt`
- TiDB Cloud index: `https://docs.pingcap.com/tidbcloud/llms.txt`
- TiDB on Kubernetes index: `https://docs.pingcap.com/tidb-in-kubernetes/llms.txt`

## Stable And Versioned URLs

- Prefer the `https://docs.pingcap.com/tidb/stable/` URL family for user-facing Self-Managed links.
- The rendered Self-Managed home can expose concrete version links such as `/tidb/v8.5/...`.
- Treat the concrete version as the current stable docs view only after checking the page selector or release mapping.
- For version-sensitive claims, fetch the user's target version explicitly.

Current stable mapping checked on 2026-06-02:

- Rendered stable home: `https://docs.pingcap.com/tidb/stable/`
- Current stable selector: `v8.5`
- Source branch: `https://github.com/pingcap/docs/tree/release-8.5`
- Self-Managed TOC: `https://raw.githubusercontent.com/pingcap/docs/release-8.5/TOC.md`

## Markdown Endpoints

Most docs pages expose a readable Markdown endpoint:

```sh
curl -fsSL https://docs.pingcap.com/tidb/stable/overview.md
curl -fsSL https://docs.pingcap.com/tidb/stable/mysql-compatibility.md
curl -fsSL https://docs.pingcap.com/tidb/stable/tidb-architecture.md
```

Rendered HTML remains useful for link extraction:

```sh
curl -fsSL https://docs.pingcap.com/tidb/stable/overview/
```

## Link Extraction

Use the bundled script when links, sidebar navigation, or body adjacency matter:

```sh
uv run --script config/codex/skills/tidb-docs/scripts/fetch_pingcap_doc_links.py https://docs.pingcap.com/tidb/stable/overview/ --docs-only
```

Useful options:

- `--article-only`: keep only links inside the main page body when the page has an `article` element.
- `--include-fragments`: preserve anchors.
- `--format json`: emit structured output.
- `--self-test`: check known docs endpoints and link relationships.

## Citation Rules

- Cite the rendered docs URL for user-facing answers unless Markdown content was the only source available.
- If a claim comes from a `.md` endpoint, cite the matching rendered page URL when possible.
- Do not cite raw GitHub TOC files for precise product behavior. Use them for routing only.
