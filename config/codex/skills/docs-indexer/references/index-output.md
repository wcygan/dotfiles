# Docs Indexer Output Guide

Use this reference when turning a crawl result into a durable docs map, source guide, or skill reference.

## Recommended Artifact Shape

For a new docs skill or research handoff, write a compact `doc-map.md`:

```markdown
# Documentation Map

Checked: YYYY-MM-DD
Source: <entry URL or folder>
Scope: <crawl boundary>

## Start Here
- <title> - <url> - why this page matters

## Core Concepts
- <title> - <url> - why this page matters

## Install, Configure, Operate
- <title> - <url> - why this page matters

## API and Reference
- <title> - <url> - why this page matters

## Troubleshooting, Migration, Limits
- <title> - <url> - why this page matters

## Notes
- Crawl limits, skipped areas, version assumptions, and pages that require manual reading.
```

## Interpreting Scores

Treat the helper's score as a reading order hint:

- High score plus clear reasons usually means the page is a good routing anchor.
- High score from inbound links alone can indicate a hub or sidebar page; read it before relying on it.
- Low score does not mean a page is unimportant for a narrow user question. Use `--focus` and rerun for topic-specific work.
- Generated indexes are not citations. Fetch and read final pages before quoting or making precise technical claims.

## Validation Checklist

- The crawl stayed within the intended docs scope.
- The top pages include an overview or introduction, a task-oriented quickstart or setup page, a concepts or architecture page, a reference/API page, and troubleshooting or migration material when those surfaces exist.
- Focused indexes rank topic-specific pages above generic docs home pages.
- Links in the final artifact are reachable or are local paths that exist.
- Versioned docs record the version or channel used, such as `stable`, `current`, `v4.3`, or a Git ref.
