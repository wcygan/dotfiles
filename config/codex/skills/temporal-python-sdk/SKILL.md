---
name: temporal-python-sdk
description: Use when building, reviewing, debugging, or documenting Python Temporal SDK code or Python Temporal applications, especially Workflows, Activities, Workers, Temporal Clients, task queues, Workflow Streams, LLM output streaming, Signals, Queries, Updates, schedules, retries, error handling, data conversion, observability, testing, sandbox determinism, sync-vs-async Activity choices, or code using the `temporalio` Python package.
---

# Temporal Python SDK

Use this skill for Python Temporal SDK work grounded in current official docs and the codebase in front of you. Keep general platform concepts in `temporal-docs`; use this skill when Python APIs, examples, or SDK-specific constraints matter.

## Workflow

1. Identify the task surface: setup/client, workflows, activities, workers, Workflow Streams, data conversion, testing/debugging, or observability.
2. Read the smallest matching reference file below.
3. Fetch the current official Temporal docs page before making precise API, version, or semantics claims. Prefer the rendered `https://docs.temporal.io/develop/python/...` page; use markdown endpoints only when they exist and are clearer.
4. Inspect local source, examples, tests, and repo instructions before editing a Python Temporal project.
5. Keep Workflow code deterministic. Put external I/O, LLM calls, network requests, random values, wall-clock time, and database calls in Activities or clients outside the Workflow.
6. For LLM output streaming, read `references/workflow-streams-llm.md` before designing or changing the pattern.

## Reference Map

- `references/doc-map.md`: Temporal Python SDK docs routing, official page shortlist, and when to use each page.
- `references/workflow-streams-llm.md`: Workflow Streams for LLM integrations, including the "Application: Stream LLM output" pattern.

## Quality Rules

- Treat this skill's references as routing guides, not frozen API docs.
- Separate Workflow state from streamed Activity output. A Workflow hosts streams but should not read its own stream.
- Prefer a single dataclass or Pydantic model input for Workflow, Activity, Signal, Query, and Update payloads when compatibility matters.
- Default to synchronous Activities for blocking Python libraries. Use async Activities only when the called code is async-safe and will not block the event loop.
- For tests, prefer integration tests with a Temporal test server when the behavior involves Workers, Workflow history, retries, timers, or message handlers.
