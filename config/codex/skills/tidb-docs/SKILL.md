---
name: tidb-docs
description: Use when answering TiDB documentation questions or locating official PingCAP docs for TiDB Self-Managed, TiDB Cloud adjacency, architecture, deployment, migration, TiCDC, DM, TiUP, TiFlash, SQL/reference, performance tuning, troubleshooting, monitoring, backup/restore, vector search, MySQL compatibility, or best practices. Fetch current docs.pingcap.com pages or llms.txt before precise claims; hand off to tidb-sql, tidb-query-tuning, or tidb-mysql for task-specific SQL, query-plan, or MySQL-compatible implementation work.
---

# TiDB Docs

Ground TiDB answers in current official PingCAP documentation and route to the smallest useful source page before making precise claims.

## Workflow

1. Identify the docs surface:
   - Use TiDB Self-Managed `stable` for general TiDB, architecture, deployment, operations, tools, SQL reference, tuning, and troubleshooting.
   - Use Developer docs for driver, ORM, connection, CRUD, schema, transaction, and application guidance.
   - Use Best Practices docs for curated deployment, schema, operations, and performance advice.
   - Use TiDB for AI docs for vector search, full-text search, hybrid search, `pytidb`, AI integrations, and MCP server pages.
   - Use TiDB Cloud or Kubernetes docs only when the user explicitly asks for managed cloud or TiDB Operator behavior.
2. Read `references/doc-map.md` to choose the smallest relevant official page.
3. Read `references/source-model.md` when URL shape, `stable` versus versioned links, rendered HTML, Markdown endpoints, or `llms.txt` routing matters.
4. Fetch current official content before exact claims. Prefer readable `.md` endpoints such as:

   ```sh
   curl -fsSL https://docs.pingcap.com/tidb/stable/overview.md
   ```

5. Use rendered HTML link extraction when page adjacency matters:

   ```sh
   uv run --script config/codex/skills/tidb-docs/scripts/fetch_pingcap_doc_links.py https://docs.pingcap.com/tidb/stable/overview/ --docs-only
   ```

6. Route to adjacent local skills when the user needs implementation rather than docs navigation:
   - `tidb-sql`: TiDB SQL generation, migration, compatibility, features, and SQL errors.
   - `tidb-query-tuning`: slow queries, plans, optimizer hints, statistics, bindings, and TiDB query incidents.
   - `tidb-mysql`: MySQL-compatible schema/index/driver review and TiDB detection behind MySQL clients.

## Official Entry Points

- Global docs index: https://docs.pingcap.com/llms.txt
- TiDB Self-Managed: https://docs.pingcap.com/tidb/stable/
- TiDB Self-Managed LLM index: https://docs.pingcap.com/tidb/llms.txt
- Developer Guide LLM index: https://docs.pingcap.com/developer/llms.txt
- Best Practices LLM index: https://docs.pingcap.com/best-practices/llms.txt
- TiDB for AI LLM index: https://docs.pingcap.com/ai/llms.txt
- API LLM index: https://docs.pingcap.com/api/llms.txt
- Source TOC for current stable: https://raw.githubusercontent.com/pingcap/docs/release-8.5/TOC.md

## Quality Rules

- Prefer official `docs.pingcap.com` pages over memory, blog posts, or third-party docs.
- Treat bundled references as routing maps, not frozen copies of the docs.
- Use `stable` URLs in user-facing answers unless the user asks about a concrete version.
- Mention version-sensitive behavior explicitly. Re-check release notes or the target version page before claiming feature availability.
- Cite the exact pages actually read when answering precise technical questions.
- Do not turn this skill into a general TiDB implementation guide. Keep implementation details in the specialized TiDB skills or in fetched official docs.

## References

- `references/doc-map.md`: topic routing for TiDB Self-Managed, Developer, Best Practices, AI, Cloud, Kubernetes, and API docs.
- `references/source-model.md`: URL patterns, `llms.txt`, Markdown endpoints, rendered HTML, source TOCs, and link extraction.
- `scripts/fetch_pingcap_doc_links.py`: link extraction and known-docs self-test.
