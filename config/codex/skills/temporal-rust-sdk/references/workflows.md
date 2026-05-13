# Workflows

Use this for workflow definitions, state, messages, timers, cancellation, determinism, and workflow API design.

Official docs:
- Workflow basics: https://docs.temporal.io/develop/rust/workflows/basics
- Client workflow starts/results: https://docs.temporal.io/develop/rust/client/temporal-client

Local anchors:
- Hello world workflow: `crates/sdk/examples/hello_world/workflows.rs:9`
- Message passing: `crates/sdk/examples/message_passing/workflows.rs:5`
- Timer examples: `crates/sdk/examples/timer_examples/workflows.rs:23`
- Cancellation examples: `crates/sdk/examples/cancellation/workflows.rs:39`
- SDK workflow module docs: `crates/sdk/src/workflows.rs:1`
- Worker registration internals: `crates/sdk/src/workflows.rs:546`
- Determinism tests: `crates/sdk-core/tests/integ_tests/workflow_tests/determinism.rs:68`

## Definition Shape

Rust workflow definitions use:
- `#[workflow]` on a struct that stores workflow state.
- `#[workflow_methods]` on an impl block.
- optional `#[init]` constructor.
- required `#[run]` async method.
- optional `#[signal]`, `#[query]`, `#[update]`, and `#[update_validator(...)]` methods.

Minimal local example:

```rust
#[workflow]
#[derive(Default)]
pub struct HelloWorldWorkflow;

#[workflow_methods]
impl HelloWorldWorkflow {
    #[run]
    pub async fn run(ctx: &mut WorkflowContext<Self>, name: String) -> WorkflowResult<String> {
        let greeting = ctx
            .start_activity(
                GreetingActivities::greet,
                name,
                ActivityOptions::start_to_close_timeout(Duration::from_secs(10)),
            )
            .await?;
        Ok(greeting)
    }
}
```

Source: `crates/sdk/examples/hello_world/workflows.rs:9`.

## Inputs and Returns

Official docs recommend structs as workflow parameters so fields can evolve without breaking the workflow signature. Inputs and returns must be serde-serializable. The workflow return type is `WorkflowResult<T>`.

Use an input struct for public workflow APIs unless the local example or test clearly benefits from a simple scalar.

## State Access

Use state APIs consistently:
- sync signals and updates may mutate through `&mut self`
- async workflow methods use `ctx.state(...)` and `ctx.state_mut(...)`
- queries are read-only and sync

Message passing anchor: `crates/sdk/examples/message_passing/workflows.rs:19`.

## Determinism Rules

Workflow code replays. Keep it deterministic:
- no direct system time; use workflow context time helpers
- no random number generation
- no external I/O such as network, filesystem, database, or a Temporal client
- no raw `tokio::select!`, `tokio::spawn`, `tokio::time::sleep`, raw tokio channels, or futures primitives that can introduce nondeterministic wake order
- put side effects in Activities

Use SDK workflow primitives:
- `ctx.timer(...)`
- `ctx.start_activity(...)`
- `ctx.start_local_activity(...)`
- `temporalio_sdk::workflows::select!`
- `temporalio_sdk::workflows::join!`
- `temporalio_sdk::workflows::join_all`

The SDK documents deterministic wrappers at `crates/sdk/src/workflows.rs:46`. The runtime nondeterminism detector is enabled by default through `WorkerOptions::detect_nondeterministic_futures` at `crates/sdk/src/lib.rs:280`.

## Timers and Races

Use `ctx.timer(Duration)` for time inside workflows. Use `workflows::select!` to race timers, cancellation, and SDK futures.

Local anchor: `crates/sdk/examples/timer_examples/workflows.rs:29`.

## Cancellation

For workflow cancellation:
- wait on `ctx.cancelled()`
- cancel pending cancellable SDK futures with `.cancel()`
- run cleanup activities if the workflow should complete gracefully

Local anchor: `crates/sdk/examples/cancellation/workflows.rs:45`.

For activity cancellation, see `activities.md`.

## Versioning and Long Histories

Use `ctx.patched("patch-id")` when evolving workflow logic that affects commands emitted during replay. Use continue-as-new when history size or long-running lifecycle requires a fresh run. Local SDK README anchors:
- patching: `crates/sdk/README.md:257`
- continue-as-new: `crates/sdk/README.md:250`

## Common Review Checks

- Is this code inside a Workflow? If yes, reject external I/O, clients, raw tokio timers, random values, and global mutable state.
- Are workflow inputs/outputs stable serde types?
- Does every activity call have suitable timeouts?
- Do task queue and workflow id come from explicit business context or a test helper?
- Are signals/queries/updates named consistently with existing workflow API style?
