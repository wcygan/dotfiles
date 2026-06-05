---
name: docs-indexer
description: Use when Codex needs to crawl, inspect, or summarize a documentation website, GitHub docs tree, or local docs folder and produce a relevance-ranked page index, doc-map, source guide, or shortlist of important documentation pages. Trigger for documentation discovery, docs indexing, source-map creation, llms.txt alternatives, docs skill scaffolding, or choosing the most relevant pages from standalone docs sites or repository documentation folders.
---

# Docs Indexer

Create a compact, evidence-backed index of the most important docs pages from a website, GitHub docs tree, or local repository folder.

## Workflow

1. Clarify the indexing target:
   - Use website mode for standalone docs sites.
   - Use GitHub tree mode for public `github.com/<owner>/<repo>/tree/<ref>/<path>` docs folders.
   - Use local mode for a checked-out repo folder or local docs directory.
2. Read `references/source-strategy.md` when source boundaries, sitemap alternatives, GitHub tree handling, or crawl scope are unclear.
3. Read `references/index-output.md` when the user needs a durable artifact such as `doc-map.md`, a source guide for another skill, or a ranked research shortlist.
4. Run the helper with a bounded crawl first:

   ```sh
   uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py <source> --max-pages 60 --top 25
   ```

5. Add `--focus "<terms>"` when the index should prioritize a topic, task, feature area, or planned skill.
6. Inspect the generated top pages and crawl notes. If the crawl was too shallow, rerun with a tighter `--scope-prefix` before raising `--max-pages`.
7. Fetch and read the highest-ranked pages before writing precise guidance. Treat the generated index as a routing artifact, not a replacement for source reading.

## Common Commands

Website docs:

```sh
uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py \
  https://docs.redpanda.com/streaming/current/home/ \
  --scope-prefix /streaming/current/ \
  --max-pages 80 \
  --top 30
```

GitHub docs folder:

```sh
uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py \
  https://github.com/openai/codex/tree/main/sdk/python/docs \
  --focus "sdk api quickstart examples" \
  --top 20
```

Local repo docs:

```sh
uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py \
  ./docs \
  --output /tmp/doc-map.md
```

Structured output:

```sh
uv run --script config/codex/skills/docs-indexer/scripts/build_docs_index.py \
  https://debezium.io/documentation/reference/stable/index.html \
  --format json \
  --output /tmp/debezium-doc-index.json
```

## Ranking Rules

- Prefer pages that are close to the seed, heavily linked by nearby docs, and named as overview, introduction, getting started, quickstart, concepts, architecture, configuration, API/reference, operations, migration, best practices, or troubleshooting.
- Use `--focus` for task-specific relevance. A focused crawl for "Kafka transactions" should rank transaction pages over generic overview pages.
- Penalize changelogs, release notes, blog posts, archives, legal pages, and search pages unless the focus terms explicitly need them.
- Keep reasons short: name the strongest title/path match, focus match, inbound links, or seed distance.

## Quality Rules

- Keep crawls bounded. Start with `--max-pages 40-80`; avoid unbounded recursive scraping.
- Stay inside the docs scope. Prefer `--scope-prefix` for websites with broad nav or marketing links.
- Respect source freshness. Re-run the helper when docs may have changed, then fetch the final pages before citing or encoding claims.
- Do not treat the helper as an authority for exact behavior, API shape, or version semantics. It ranks pages; Codex still needs to read the pages it uses.
- For private repos, use a local checkout instead of adding tokens or credentials to the script invocation.

## Resources

- `scripts/build_docs_index.py`: bounded crawler and relevance-ranked Markdown/JSON index generator.
- `references/source-strategy.md`: source selection, crawl boundaries, website/GitHub/local handling, and failure modes.
- `references/index-output.md`: recommended index artifact shape, ranking interpretation, and validation checklist.
