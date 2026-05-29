---
name: temporal-docs
description: "Use when explaining, designing, reviewing, or debugging general Temporal concepts from docs.temporal.io, including Temporal Platform architecture, Workflows, Workflow Execution, Activities, Workers, Event History, failure detection, Workflow message passing, Child Workflows, Temporal Service, Namespaces, Task Queues, durable execution, replay, determinism, Signals, Queries, Updates, retries, and timeouts. Fetch current official Temporal docs and inspect embedded page links before giving precise guidance; use SDK-specific skills only when exact language APIs or code semantics are the main task."
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Temporal Docs

Goal: Ground general Temporal answers in the current official docs and the concept graph those docs expose.

Success means:
- The answer uses official `https://docs.temporal.io/` pages as the source of truth.
- The agent inspects rendered HTML links when page adjacency matters.
- The agent separates high-level platform concepts from SDK-specific API details.

Stop when the user has a conceptually correct answer, design review, or navigation path with exact Temporal docs links.

## Workflow

1. Identify the Temporal concept surface: platform overview, Workflows, Workflow Execution, Activities, Workers, Event History, failure detection, message passing, Child Workflows, Temporal Service, Namespaces, or an adjacent concept.
2. Read `references/doc-map.md` to choose the smallest relevant reference file.
3. Load the topic reference file for the concept being explained or reviewed.
4. Fetch the current official page before making precise claims. Prefer `https://docs.temporal.io/<path>.md` for readable page content when it exists.
5. Inspect rendered HTML links when the user asks what a page points to, when a page is a hub, or when the next source is unclear. Use `scripts/fetch_temporal_doc_links.py` or another structured HTML parser.
6. Follow concept links one hop at a time. Keep the answer anchored to the specific docs pages that were actually read.
7. Use SDK-specific docs only for language API syntax, package setup, or code examples. Keep this skill focused on platform semantics and cross-SDK concepts.

## Source Model

- Rendered docs root: `https://docs.temporal.io/`
- LLM markdown pattern for most pages: `https://docs.temporal.io/<path>.md`
- Rendered HTML is the source for embedded hyperlinks, sidebar adjacency, page hierarchy, and anchors.
- Raw MDX in `temporalio/documentation` is useful when a rendered directory page lacks a `.md` endpoint; cite the rendered docs URL in user-facing answers.

## Link Extraction

Use the bundled script for repeatable link discovery:

```sh
uv run --script config/claude/skills/temporal-docs/scripts/fetch_temporal_doc_links.py https://docs.temporal.io/workflows --docs-only
```

Add `--article-only` when the answer should cover only links in the main page body and exclude shared navigation.
Use `--include-fragments` when anchors matter, such as `https://docs.temporal.io/workflow-execution/workflowid-runid#workflow-id`.
Run `--self-test` after editing references or expected link relationships.

## Reference Map

- `references/doc-map.md`: concept routing and official docs index.
- `references/html-link-navigation.md`: rendered HTML, markdown endpoints, raw MDX fallbacks, and link extraction rules.
- `references/temporal-platform.md`: Temporal Platform, Applications, Service, Workers, SDKs, and high-level topology.
- `references/workflows.md`: Workflows, Workflow Definitions, replay, determinism, and adjacent workflow pages.
- `references/workflow-execution.md`: Workflow Execution, Workflow ID and Run ID, Events, Continue-As-New, limits, timers, status, and chains.
- `references/activities.md`: Activities, Activity Definition, Activity Execution, Local Activities, Standalone Activities, idempotency, and Activity Events.
- `references/application-failures.md`: detecting Activity and Workflow failures, retries, timeouts, heartbeats, and failure boundaries.
- `references/workers.md`: Worker Program, Worker Process, Worker Entity, Worker Identity, Task Queues, polling, and tuning.
- `references/event-history.md`: Event History, Commands, replay, history growth, and language walkthrough links.
- `references/workflow-message-passing.md`: Signals, Queries, Updates, handlers, validators, and choosing message types.
- `references/child-workflows.md`: Child Workflow Executions, parent close policy, cancellation, and decomposition boundaries.
- `references/temporal-service.md`: Frontend, History, Matching, Worker Services, persistence, visibility, and service topology.
- `references/namespaces.md`: Namespaces, isolation, retention, archival, registration, and operational boundaries.

## Quality Rules

- Prefer official Temporal docs over memory or blog posts for definitions and current page relationships.
- Treat bundled references as routing guides, not frozen copies of the docs.
- Name the exact page and link used for each precise claim.
- Explain concepts in SDK-neutral language first, then point to SDK pages only when implementation details are needed.
- Preserve Temporal's key distinctions: Workflow Definition vs Workflow Execution, Activity Definition vs Activity Execution, Worker Program vs Worker Process vs Worker Entity, and Temporal Service vs Worker.
