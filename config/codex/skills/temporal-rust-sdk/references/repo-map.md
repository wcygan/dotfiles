# sdk-rust Repo Map

These anchors assume repo root `/Users/wcygan/Development/sdk-rust`. If working in another checkout, use the same repo-relative paths.

## Workspace Layout

- `crates/sdk`: application-facing Rust SDK built on Core. Start here for workflows, activities, workers, examples, and macro-driven API usage.
- `crates/client`: Rust client for Temporal service operations such as start, signal, query, update, cancel, describe, and history fetch.
- `crates/common`: shared data converters, telemetry, envconfig, protobufs, payload helpers, and common worker/client types.
- `crates/macros`: procedural macros for workflows and activities.
- `crates/sdk-core`: Core SDK implementation, pollers, workflow/activity state machines, replay, test helpers, and integration tests.
- `crates/sdk-core-c-bridge`: C bridge for other language SDKs.

Repo anchors: `README.md:41`, `AGENTS.md:72`.

## Canonical Examples

- Hello world workflow and activity: `crates/sdk/examples/hello_world/workflows.rs:9`.
- Hello world worker with envconfig and registration: `crates/sdk/examples/hello_world/worker.rs:13`.
- Hello world starter with `start_workflow` and `get_result`: `crates/sdk/examples/hello_world/starter.rs:11`.
- Activity heartbeating and retry checkpoint resume: `crates/sdk/examples/activity_heartbeating/workflows.rs:10`.
- Signal, query, update, and update validator: `crates/sdk/examples/message_passing/workflows.rs:5`.
- Child workflows: `crates/sdk/examples/child_workflows/workflows.rs:17`.
- Workflow and activity cancellation: `crates/sdk/examples/cancellation/workflows.rs:9`.
- Local activities beside remote activities: `crates/sdk/examples/local_activities/workflows.rs:30`.
- Timers, deterministic `select!`, and cancellable timers: `crates/sdk/examples/timer_examples/workflows.rs:23`.

## Public SDK API Anchors

- SDK public preview warning and crate overview: `crates/sdk/src/lib.rs:3`.
- Re-exported workflow/activity/client-facing types: `crates/sdk/src/lib.rs:100`.
- `WorkerOptions` fields and defaults: `crates/sdk/src/lib.rs:182`.
- `WorkerOptions` builder registration helpers: `crates/sdk/src/lib.rs:287`.
- `Worker::new` runtime/client/options wiring: `crates/sdk/src/lib.rs:468`.
- `Worker::run` polling and execution loop entry point: `crates/sdk/src/lib.rs:593`.
- Workflow module macro model and deterministic wrappers: `crates/sdk/src/workflows.rs:1`.
- Workflow registration internals: `crates/sdk/src/workflows.rs:546`.
- Activity module and `ActivityContext`: `crates/sdk/src/activities.rs:1`, `crates/sdk/src/activities.rs:74`.

## Client and Configuration Anchors

- Client README quickstart and envconfig example: `crates/client/README.md:15`.
- Client signal/query/update examples: `crates/client/README.md:87`.
- `ConnectionOptions` surface: `crates/client/src/options_structs.rs:22`.
- Supported env vars and TOML shape: `crates/common/src/envconfig.rs:7`.
- Config resolution order: `crates/common/src/envconfig.rs:304`.
- Env override application: `crates/common/src/envconfig.rs:412`.
- `ClientOptions::load_from_config` bridge: `crates/client/src/envconfig.rs:19`.
- Profile-to-client conversion: `crates/client/src/envconfig.rs:107`.
- Address parsing and TLS defaults: `crates/client/src/envconfig.rs:43`.
- `WorkflowStartOptions` fields: `crates/client/src/options_structs.rs:198`.

## Tests and Debugging Anchors

- Coding-agent command rules: `AGENTS.md:6`.
- PR build/test command list: `README.md:54`.
- Tracing setup for debugging: `README.md:82`.
- History fetch tool: `README.md:126`.
- Integration runner behavior: `crates/sdk-core/tests/runner.rs:55`.
- Integration `CoreWfStarter` pattern: `crates/sdk-core/tests/common/mod.rs:238`.
- `TestWorker` registration/submission/run-until-done pattern: `crates/sdk-core/tests/common/mod.rs:504`.
- Compact integration workflow/activity test: `crates/sdk-core/tests/integ_tests/workflow_tests/activities.rs:99`.
- Integration test helpers and fake workers: `crates/sdk-core/src/test_help/integ_helpers.rs:1`.
- Determinism and replay integration tests: `crates/sdk-core/tests/integ_tests/workflow_tests/determinism.rs:68`.
- Nondeterministic future detector test: `crates/sdk-core/tests/integ_tests/workflow_tests/determinism.rs:481`.
- Replay worker input and history feeder: `crates/sdk-core/src/replay/mod.rs:53`.
- SDK replay test setup: `crates/sdk-core/tests/integ_tests/workflow_tests/replay.rs:34`.
- History fetch CLI source: `crates/sdk-core/src/histfetch.rs:1`.

## Command Rules In This Repo

- Run integration tests only with `cargo integ-test <test_name>`. Use `timeout 180 cargo integ-test <test_name>` for risky hang-prone changes after compilation.
- Run unit tests with `cargo test`.
- Run lints with `cargo lint`, not `cargo clippy`.
- Run test lints with `cargo test-lint`.
- Format with `cargo +nightly fmt`.
- Do not run `cargo test --test heavy_tests` unless the user explicitly asks.
