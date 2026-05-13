# Temporal Rust SDK Documentation Map

Use this file to choose the smallest official source before giving precise Rust Temporal SDK guidance.

## Official Docs

- Rust SDK developer guide: https://docs.temporal.io/develop/rust
  - Hub page for Rust workflows, activities, workers, client, Nexus, docs.rs, and the SDK GitHub repo.
- Quickstart: https://docs.temporal.io/develop/rust/quickstart
  - Local setup, Rust/Cargo, SDK dependencies, Temporal CLI dev server, hello-world workflow/activity/worker flow.
- Workflow basics: https://docs.temporal.io/develop/rust/workflows/basics
  - `#[workflow]`, `#[workflow_methods]`, `#[init]`, `#[run]`, parameters, return values, workflow type naming, deterministic execution constraints.
- Child Workflows: https://docs.temporal.io/develop/rust/workflows/child-workflows
  - `ctx.child_workflow()`, `PendingChildWorkflow`, child workflow options, parallel child workflows, parent close policy.
- Continue-As-New: https://docs.temporal.io/develop/rust/workflows/continue-as-new
  - using continue-as-new to reset event history, carrying state into the next run, and testing continue-as-new behavior.
- Workflow message passing: https://docs.temporal.io/develop/rust/workflows/message-passing
  - query, signal, update, update validator, async handlers, and client-side message APIs.
- Workflow cancellation: https://docs.temporal.io/develop/rust/workflows/cancellation
  - cancellation handling and cleanup patterns.
- Workflow timers: https://docs.temporal.io/develop/rust/workflows/timers
  - `ctx.timer()` and timer cancellation.
- Workflow timeouts: https://docs.temporal.io/develop/rust/workflows/timeouts
  - workflow execution/run/task timeouts and workflow retry policy guidance.
- Activity basics: https://docs.temporal.io/develop/rust/activities/basics
  - `#[activities]`, `#[activity]`, `ActivityContext`, `ActivityError`, `Arc<Self>` activities, serde parameters, return values, application failures.
- Activity execution: https://docs.temporal.io/develop/rust/activities/execution
  - workflow-side activity execution options, timeouts, retry policy, local activities if present in current docs.
- Activity timeouts: https://docs.temporal.io/develop/rust/activities/timeouts
  - activity timeout fields, retry policy, heartbeat timeout, heartbeat details, and cancellation delivery through heartbeats.
- Worker processes: https://docs.temporal.io/develop/rust/workers/worker-process
  - Worker process, worker entity, task queue registration rules, `WorkerOptions`, `Worker::new`, and `run()`.
- Temporal Client: https://docs.temporal.io/develop/rust/client/temporal-client
  - `Connection`, `Client`, env/config loading, Cloud connection, `start_workflow`, `WorkflowStartOptions`, workflow id, task queue, `get_result`.
- Environment configuration: https://docs.temporal.io/develop/environment-configuration
  - Cross-SDK environment configuration model. For Rust-specific variable names and conversion rules, prefer local `crates/common/src/envconfig.rs` and `crates/client/src/envconfig.rs`.
- Rust API docs: https://docs.rs/temporalio-sdk and https://docs.rs/temporalio-client
  - Use for exact signatures when local source is unavailable or the target project depends on a released crate instead of this workspace.

## Verification Rules

- Fetch the official page when answering questions about exact syntax, currently recommended setup, public API names, dependency versions, Temporal Cloud auth, or environment variable behavior.
- Check local `Cargo.toml`, examples, and source when editing this repo. The docs may describe a released version while the checkout may contain unreleased API changes.
- For SDK internals or tests, trust local code over docs. The official docs cover the application-facing SDK model, not every core/internal helper.
- Avoid long quotes from docs. Summarize and link the exact page instead.

## Local Docs Anchors

- `README.md:41` maps the workspace crates.
- `README.md:54` lists PR build/test commands.
- `README.md:82` describes tracing for debugging.
- `README.md:126` describes fetching histories with `cargo run --bin histfetch`.
- `crates/sdk/README.md:6` states that the Rust SDK is Public Preview.
- `crates/client/README.md:6` states that `temporalio-client` can be used standalone or with `temporalio-sdk`.
