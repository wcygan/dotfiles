---
name: temporal-rust-sdk
description: Use when building, reviewing, debugging, or documenting Rust Temporal SDK code or Rust Temporal applications, especially workflows, activities, workers, Temporal clients, environment configuration, task queues, workflow history/replay, nondeterminism, and tests in temporalio/sdk-rust or code using temporalio-sdk, temporalio-client, temporalio-common, temporalio-macros, or temporalio-sdk-core.
---

# Temporal Rust SDK

Use this skill for Rust Temporal SDK work grounded in the current codebase and official Temporal docs. Keep this file thin: load the smallest relevant reference file from the map below, then inspect nearby repo code before editing.

## Workflow

1. Identify the task surface: setup/client, workflows, activities, workers, advanced workflow behavior, tests/debugging, or repo navigation.
2. Read the matching reference file below. If exact APIs, versions, or current recommendations matter, fetch the linked official Temporal docs before making a precise claim.
3. Inspect the relevant local source, examples, tests, and `AGENTS.md` in the target repo before changing code.
4. Follow existing Rust style and repo rules. In `sdk-rust`, use `cargo integ-test <test_name>` for integration tests, `cargo lint` for clippy, and `cargo +nightly fmt` for formatting.
5. Prefer deterministic workflow primitives and activities for side effects. Do not put client creation, external I/O, random values, direct system time, or raw tokio/futures concurrency in Workflow code.

## Reference Map

- `references/doc-map.md`: official Temporal docs index and when to verify docs.rs or live docs.
- `references/documentation-explorer.md`: how to inspect Temporal's rendered docs and matching raw MDX sources in `temporalio/documentation`.
- `references/repo-map.md`: sdk-rust crate layout, high-value local code anchors, and repo command rules.
- `references/setup-env-client.md`: quickstart setup, dependencies, Temporal CLI dev server, env/config loading, Cloud connection, starting workflows, results, signals, queries, and updates.
- `references/workflows.md`: workflow macros, inputs/returns, deterministic execution, state access, messages, timers, cancellation, continue-as-new, patching, and common gotchas.
- `references/workflow-patterns.md`: child workflows, message passing, local activities, timers, cancellation, continue-as-new, workflow timeouts/retries, and public workflow-context APIs.
- `references/activities.md`: activity macros, signatures, `ActivityContext`, heartbeats, cancellation, errors, payload limits, local activities, and stateful activity implementers.
- `references/workers.md`: worker process model, task queues, registration, `WorkerOptions`, runtime/client wiring, task type selection, worker identity, shutdown, and tuning entry points.
- `references/testing-debugging.md`: sdk-rust test commands, integration helpers, replay/history tools, nondeterminism debugging, tracing, and test style constraints.

## Quality Rules

- Treat `crates/sdk/README.md` and the example programs as living SDK examples, but verify public API details against official docs or current local source because the Rust SDK is Public Preview.
- Keep code examples aligned with the project in front of you: imports at file or test-module scope, existing builder style, existing data converter patterns, and existing test helpers.
- Do not add explicit sleeps to tests when synchronization can be expressed with channels, `Notify`, semaphores, handles, or harness state.
- Add comments only when they explain a non-obvious reason.
