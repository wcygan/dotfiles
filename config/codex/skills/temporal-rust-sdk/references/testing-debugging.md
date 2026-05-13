# Testing and Debugging

Use this for sdk-rust tests, integration-test commands, replay/history debugging, nondeterminism failures, telemetry, and review checklists.

Local anchors:
- Agent rules: `AGENTS.md:6`
- PR commands: `README.md:54`
- Debugging/tracing: `README.md:82`
- History fetch: `README.md:126`
- Integration runner: `crates/sdk-core/tests/runner.rs:55`
- Integration `CoreWfStarter`: `crates/sdk-core/tests/common/mod.rs:238`
- `TestWorker`: `crates/sdk-core/tests/common/mod.rs:504`
- Compact workflow/activity integration test: `crates/sdk-core/tests/integ_tests/workflow_tests/activities.rs:99`
- Integration helpers: `crates/sdk-core/src/test_help/integ_helpers.rs:1`
- Determinism tests: `crates/sdk-core/tests/integ_tests/workflow_tests/determinism.rs:68`
- Nondeterministic future detector test: `crates/sdk-core/tests/integ_tests/workflow_tests/determinism.rs:481`
- Replay worker input and history feeder: `crates/sdk-core/src/replay/mod.rs:53`
- SDK replay tests: `crates/sdk-core/tests/integ_tests/workflow_tests/replay.rs:34`

## Commands

Use repo commands exactly:
- format: `cargo +nightly fmt`
- unit tests: `cargo test`
- lints: `cargo lint`
- test lints: `cargo test-lint`
- integration tests: `cargo integ-test <test_name>`
- hang-prone integration checks after compilation: `timeout 180 cargo integ-test <test_name>`

Do not run integration tests directly. Do not run `cargo clippy` directly. Do not run `cargo test --test heavy_tests` unless the user explicitly asks.

## Test Style

Follow `AGENTS.md`:
- Do not put `use` statements in function scope unless needed for trait ambiguity.
- Avoid explicit sleeps in test code. Prefer channels, `Notify`, semaphores, worker handles, task completion, or harness state.
- If debugging with `dbg!` or `println!` in an integration test, use `cargo integ-test <test_name> -- --nocapture` to see output.
- Some tests intentionally panic. Treat the harness result as authoritative.

## Integration Helpers

Start with `crates/sdk-core/src/test_help/integ_helpers.rs` and nearby `crates/sdk-core/tests/integ_tests`.

Useful concepts:
- `CoreWfStarter` and starter helpers create task queues and clients for integration tests.
- worker helpers register workflows and activities, submit workflows, and run workers until done.
- fake worker helpers build mock pollers and histories for core-level behavior.

When adding a new integration test, mirror the closest existing test file instead of inventing a new harness shape.

The compact pattern is visible at `crates/sdk-core/tests/integ_tests/workflow_tests/activities.rs:99`:
1. create `CoreWfStarter`
2. register activities and workflow on `starter.sdk_config`
3. call `starter.worker().await`
4. submit the workflow through the `TestWorker`
5. `worker.run_until_done().await`
6. assert the workflow result

## Nondeterminism Debugging

Workflow nondeterminism usually comes from:
- using raw tokio/futures primitives in workflow code
- system time, random values, external I/O, or global mutable state
- changing command-emitting workflow logic without patching/versioning
- changing activity or child workflow type/id/command order incompatibly with existing history

The SDK has a runtime nondeterminism detector enabled by default. The test at `crates/sdk-core/tests/integ_tests/workflow_tests/determinism.rs:481` shows a raw `tokio::time::sleep` raced against a workflow timer causing a Workflow Task failure recorded in history.

When debugging:
1. Check whether the failing code runs inside a Workflow.
2. Replace raw async/time/concurrency with SDK workflow primitives.
3. Fetch or inspect history when replay behavior matters.
4. Add a targeted determinism or replay test when changing workflow execution semantics.

## Histories and Replay

Fetch histories with:

```bash
cargo run --bin histfetch <workflow_id> [run_id]
```

The README notes `TEMPORAL_SERVICE_ADDRESS` can point the history fetcher at a different service. Anchor: `README.md:126`.

Replay helpers live under `crates/sdk-core/src/replay` and appear in determinism tests through `TestHistoryBuilder` and canned histories. Use replay tests for changes where command ordering or event interpretation matters.

For SDK replay tests, inspect `crates/sdk-core/tests/integ_tests/workflow_tests/replay.rs:34`. For lower-level replay primitives, inspect `ReplayWorkerInput`, `HistoryForReplay`, and `HistoryFeeder` in `crates/sdk-core/src/replay/mod.rs:53`.

## Tracing

The repo uses `tracing`. README anchor: `README.md:82`.

For tests, initialize tracing early with the existing helper pattern from nearby tests. For integration tests with OpenTelemetry collection, use the repo-provided script and docker-compose files rather than adding ad hoc telemetry setup.

## Review Checklist

- Did the change touch workflow logic? Check determinism and replay implications.
- Did the change touch activity heartbeat/cancellation? Add a cancellation or retry checkpoint test if behavior changes.
- Did the change touch worker polling/tuning/shutdown? Use focused integration tests and avoid time-based assertions.
- Did the change touch envconfig/client setup? Cover env var precedence, TOML parsing, TLS/API key edge cases, and secret redaction where relevant.
- Did the change touch public API? Update examples/docs and ensure comments explain why, not what.
