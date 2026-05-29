# HTML Link Navigation

Use this reference when a task depends on the links embedded in a Temporal docs page, including sidebar links, page-local tables of contents, adjacent pages, and anchors.

## Fetch Strategy

1. Fetch rendered HTML for link discovery:

   ```sh
   uv run --script config/claude/skills/temporal-docs/scripts/fetch_temporal_doc_links.py https://docs.temporal.io/workflows --docs-only
   ```

   Add `--article-only` to inspect links in the main docs page body without global navigation and sidebar links.

2. Fetch LLM markdown for readable page content when available:

   ```sh
   curl -Ls https://docs.temporal.io/workflows.md
   ```

3. Use raw MDX only when the rendered page lacks a `.md` endpoint. Known examples:

   ```text
   https://docs.temporal.io/encyclopedia/event-history/
   https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/event-history/event-history.mdx

   https://docs.temporal.io/encyclopedia/workflow-message-passing/
   https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/workflow-message-passing/workflow-message-passing.mdx
   ```

## Link Handling Rules

- Normalize relative paths against `https://docs.temporal.io/`.
- Keep fragments when the anchor is the point of the question, such as `/workflow-execution/workflowid-runid#workflow-id`.
- Remove fragments when building a page-level map.
- Keep sidebar links when the user asks what page relationships or navigation links exist.
- Prefer page-body links when the user asks what the page text recommends reading next.
- Filter static assets such as `/assets/`, `/img/`, `/scripts/`, and `/diagrams/` when building concept maps.

## Known Concept Graph Examples

`https://docs.temporal.io/workflows` links to:

- https://docs.temporal.io/workflow-definition
- https://docs.temporal.io/workflow-execution
- https://docs.temporal.io/schedule
- https://docs.temporal.io/dynamic-handler
- https://docs.temporal.io/cron-job

`https://docs.temporal.io/workflow-execution` links to:

- https://docs.temporal.io/workflow-execution/workflowid-runid
- https://docs.temporal.io/workflow-execution/event
- https://docs.temporal.io/workflow-execution/continue-as-new
- https://docs.temporal.io/workflow-execution/limits
- https://docs.temporal.io/workflow-execution/timers-delays
- https://docs.temporal.io/encyclopedia/event-history/

## Script Output Shapes

Markdown output is easiest for quick review:

```sh
uv run --script config/claude/skills/temporal-docs/scripts/fetch_temporal_doc_links.py https://docs.temporal.io/workflow-execution --docs-only --include-fragments
```

JSON output is easiest for downstream processing:

```sh
uv run --script config/claude/skills/temporal-docs/scripts/fetch_temporal_doc_links.py https://docs.temporal.io/workflow-execution --docs-only --format json
```

Run the known-docs self-test after changing this skill's source map:

```sh
uv run --script config/claude/skills/temporal-docs/scripts/fetch_temporal_doc_links.py --self-test
```
