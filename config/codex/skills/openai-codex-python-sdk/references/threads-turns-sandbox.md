---
canonical_url: https://github.com/openai/codex/blob/main/sdk/python/docs/api-reference.md
last_verified: 2026-06-05
---

# Threads, Turns, and Sandbox

Use this reference for application structure and API shape. Re-read the API reference before exact signatures.

## Client Shape

- `Codex` is the sync client.
- `AsyncCodex` is the async counterpart with the same public API shape.
- Prefer `with Codex() as codex:` for sync code.
- Prefer `async with AsyncCodex() as codex:` for async code.

The public package exports the client classes, config, approval and sandbox enums, login handles, thread and turn handles, input types, and selected protocol types under `openai_codex.types`.

## Thread Lifecycle

A `Thread` is conversation state. A turn is one model execution inside that thread.

Common lifecycle calls include:

- `thread_start(...)` to create a new thread.
- `thread_resume(thread_id, ...)` to continue an existing thread.
- `thread_list(...)`, `thread_fork(...)`, `thread_archive(...)`, and `thread_unarchive(...)` for thread management.
- `models(...)` to list visible models for the connected runtime.

The public API keeps lifecycle calls explicit; do not invent aliases or wrapper names unless the target app already has them.

## Running Turns

Use `Thread.run(...)` for the common path. It accepts plain strings for text-only turns, starts the turn, waits for completion, and returns a `TurnResult`.

Use `Thread.turn(...)` when the application needs low-level control before collecting the result:

- `stream()` for raw notifications and progress UI.
- `steer()` for active-turn steering.
- `interrupt()` for cancellation or interruption flows.
- `run()` on a turn handle to consume events and return the same `TurnResult` shape.

For async code, the corresponding `AsyncThread` and `AsyncTurnHandle` methods return awaitables or async streams.

## Result Shape

The API reference lists `TurnResult` fields such as:

- `id`
- `status`
- `error`
- `started_at`
- `completed_at`
- `duration_ms`
- `final_response`
- `items`
- `usage`

`final_response` can be `None` when a turn finishes without a final-answer or phase-less assistant message item. Check that case explicitly in application code.

## Sandbox Access

Use the same `sandbox=` keyword for thread lifecycle methods and turns:

- `Sandbox.read_only`: read files without writes.
- `Sandbox.workspace_write`: read and write inside the workspace and configured writable roots.
- `Sandbox.full_access`: run without filesystem access restrictions.

When omitted, Codex uses its configured default. The docs note that a turn sandbox override also applies to subsequent turns on that thread, so avoid using a broad sandbox for one turn and assuming later turns reset automatically.

## Keyword Arguments

Public Python keyword arguments are `snake_case`. The SDK maps wire-level camelCase internally. When migrating older snippets, check the FAQ mapping before editing.
