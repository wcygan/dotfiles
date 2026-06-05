---
canonical_url: https://github.com/openai/codex/blob/main/sdk/python/docs/faq.md
last_verified: 2026-06-05
---

# Troubleshooting

Use this reference for failure handling, migration, and behavioral questions. Verify against the current FAQ or local SDK source before making durable changes.

## Beta Stability

The docs describe `openai-codex` as a public beta. Public APIs may change before `1.0`, so pin versions for production-like apps and keep examples close to the installed package.

## `run()` vs `stream()`

- `Thread.run(...)` starts a turn and returns `TurnResult`.
- `TurnHandle.run()` and `AsyncTurnHandle.run()` consume events for an existing turn handle and return the same `TurnResult` shape.
- `TurnHandle.stream()` and `AsyncTurnHandle.stream()` yield raw notifications for event-by-event handling.

Choose `run()` for most apps. Choose `stream()` only for progress UIs, custom timeout logic, or custom parsing, and keep consuming notifications until the matching turn completes.

## Sync vs Async

- `Codex` is the sync public API.
- `AsyncCodex` mirrors the public API for async code.
- Use `async with AsyncCodex()` when already inside an async application.
- Stay with `Codex` when the application is not otherwise async.

## Migration Notes

Public keyword names are `snake_case`. Older camelCase snippets should be updated. Common mappings include:

- `baseInstructions` -> `base_instructions`
- `developerInstructions` -> `developer_instructions`
- `modelProvider` -> `model_provider`
- `modelProviders` -> `model_providers`
- `sortKey` -> `sort_key`
- `sourceKinds` -> `source_kinds`
- `outputSchema` -> `output_schema`

## Constructor Failures

Common causes include:

- incomplete installation with missing pinned `openai-codex-cli-bin`
- a local `codex_bin` override pointing to a missing file
- a custom local Codex executable that does not support the SDK operation being used

Check package metadata, installed files, and any local runtime overrides before editing application code.

## Hanging Turns

A turn is complete only when the matching `turn/completed` notification arrives. `run()` waits for this automatically. With `stream()`, continue consuming notifications until completion.

## Retry Policy

Use the SDK-supported overload retry pattern for transient overload failures such as `ServerBusyError`. Do not blindly retry all errors. For `InvalidParamsError` or `MethodNotFoundError`, fix the input or use the runtime pinned by the SDK.
