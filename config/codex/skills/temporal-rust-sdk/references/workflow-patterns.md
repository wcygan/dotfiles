# Workflow Patterns

Use this after `workflows.md` when the task involves child workflows, message passing, local activities, timers, cancellation, continue-as-new, timeouts, or workflow-context APIs.

Official docs:
- Child workflows: https://docs.temporal.io/develop/rust/workflows/child-workflows
- Continue-As-New: https://docs.temporal.io/develop/rust/workflows/continue-as-new
- Workflow message passing: https://docs.temporal.io/develop/rust/workflows/message-passing
- Workflow cancellation: https://docs.temporal.io/develop/rust/workflows/cancellation
- Workflow timers: https://docs.temporal.io/develop/rust/workflows/timers
- Workflow timeouts: https://docs.temporal.io/develop/rust/workflows/timeouts

Local anchors:
- Child workflows example: `crates/sdk/examples/child_workflows/workflows.rs:17`
- Message passing example: `crates/sdk/examples/message_passing/workflows.rs:5`
- Local activities example: `crates/sdk/examples/local_activities/workflows.rs:30`
- Cancellation example: `crates/sdk/examples/cancellation/workflows.rs:39`
- Timer example: `crates/sdk/examples/timer_examples/workflows.rs:23`
- Public workflow context APIs: `crates/sdk/src/workflow_context.rs:715`
- Trybuild workflow signatures: `crates/sdk-core/tests/workflows_trybuild/basic_pass.rs:4`

## Child Workflows

Use `ctx.child_workflow()` inside a workflow when a child execution should be visible in the parent's event history and have its own workflow lifecycle.

Local example:

```rust
let started = ctx
    .child_workflow(
        GreetingChildWorkflow::run,
        name.clone(),
        ChildWorkflowOptions {
            workflow_id: format!("greeting-child-{i}"),
            ..Default::default()
        },
    )
    .await?;

let greeting = started.result().await?;
```

Source: `crates/sdk/examples/child_workflows/workflows.rs:30`.

Official docs emphasize waiting until the child workflow has started before moving on. Use `ChildWorkflowOptions` for workflow id and parent close policy. Parent close policy choices are terminate, abandon, or request cancel.

## Message Passing

Queries, signals, and updates are workflow methods:
- query: sync, read-only, cannot mutate workflow state
- signal: asynchronous message, usually mutates state and returns no value
- update: trackable request that can mutate state and return a result
- update validator: rejects invalid update input before acceptance is recorded in history

Local compact example: `crates/sdk/examples/message_passing/workflows.rs:19`.

Prefer serde structs for handler inputs when public APIs may evolve. The official message-passing docs recommend structs over multiple parameters for forward-compatible changes.

## Local Activities

Use local activities for short-lived activity work that should execute on the same worker as the workflow. Compare remote and local activity calls in `crates/sdk/examples/local_activities/workflows.rs:30`.

Remote activity:

```rust
ctx.start_activity(
    GreetingActivities::greet,
    name.clone(),
    ActivityOptions::start_to_close_timeout(Duration::from_secs(10)),
).await?;
```

Local activity:

```rust
ctx.start_local_activity(
    GreetingActivities::greet,
    name,
    LocalActivityOptions {
        start_to_close_timeout: Some(Duration::from_secs(10)),
        ..Default::default()
    },
).await?;
```

Review local activities carefully because they trade server scheduling semantics for worker-local execution.

## Timers and Cancellation

Use `ctx.timer(...)`, not `tokio::time::sleep(...)`, inside workflows. Use `temporalio_sdk::workflows::select!` for deterministic races.

Timer anchor: `crates/sdk/examples/timer_examples/workflows.rs:29`.

Cancellation anchor: `crates/sdk/examples/cancellation/workflows.rs:45`.

Cancellation pattern:
- create a cancellable SDK future
- race it with `ctx.cancelled()`
- call `.cancel()` on the pending future when cancellation wins
- run cleanup through an Activity if cleanup has side effects

## Continue-As-New

Use continue-as-new when a workflow needs a fresh event history, commonly for very long-running loops or batch processing. Carry all state needed by the next run in serializable input.

The SDK README anchors `ctx.continue_as_new(&new_input, ContinueAsNewOptions::default())` at `crates/sdk/README.md:250`. Official docs also recommend testing continue-as-new with a test hook or a small history threshold instead of waiting for natural production limits.

## Workflow Timeouts and Retries

Official docs caution that workflow timeouts are usually not recommended because workflows are designed to be long-running and resilient. Prefer workflow timers for business deadlines.

When a timeout or workflow retry policy is intentional, set it on `WorkflowStartOptions`; exact fields are in `crates/client/src/options_structs.rs:198`:
- `execution_timeout`
- `run_timeout`
- `task_timeout`
- `retry_policy`

Apply workflow retry policies only when restarting the entire workflow is safe and intentional.

## Context API Search Hints

If the exact method name matters, search `crates/sdk/src/workflow_context.rs` for:
- `pub fn timer`
- `pub fn start_activity`
- `pub fn start_local_activity`
- `pub fn child_workflow`
- `continue_as_new`
- `cancelled`
- `history_length`
- `continue_as_new_suggested`
