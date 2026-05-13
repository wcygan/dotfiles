# Activities

Use this for activity definitions, heartbeats, retries, cancellation, error handling, payloads, and local activities.

Official docs:
- Activity basics: https://docs.temporal.io/develop/rust/activities/basics
- Activity execution: https://docs.temporal.io/develop/rust/activities/execution
- Activity timeouts: https://docs.temporal.io/develop/rust/activities/timeouts

Local anchors:
- Hello world activity: `crates/sdk/examples/hello_world/workflows.rs:28`
- Heartbeating activity: `crates/sdk/examples/activity_heartbeating/workflows.rs:10`
- Workflow-side heartbeat timeout configuration: `crates/sdk/examples/activity_heartbeating/workflows.rs:45`
- Cancellation activity: `crates/sdk/examples/cancellation/workflows.rs:9`
- Local activities beside remote activities: `crates/sdk/examples/local_activities/workflows.rs:30`
- Activity module docs and `ActivityContext`: `crates/sdk/src/activities.rs:1`, `crates/sdk/src/activities.rs:74`
- Trybuild activity signatures: `crates/sdk-core/tests/activities_trybuild/basic_pass.rs:7`
- Activity details in SDK README: `crates/sdk/README.md:285`

## Definition Shape

Rust activity definitions use:
- `#[activities]` on an impl block.
- `#[activity]` on public async methods.
- `ActivityContext` as the first parameter.
- `Result<T, ActivityError>` as the return type.
- serde-serializable inputs and outputs.

Minimal local example:

```rust
pub struct GreetingActivities;

#[activities]
impl GreetingActivities {
    #[activity]
    pub async fn greet(_ctx: ActivityContext, name: String) -> Result<String, ActivityError> {
        Ok(format!("Hello, {}!", name))
    }
}
```

Source: `crates/sdk/examples/hello_world/workflows.rs:28`.

## Stateful Activities

Activities can take `self: Arc<Self>` for shared state. The SDK activity docs include this shape, and the local module documents it at `crates/sdk/src/activities.rs:24`.

Use shared state for worker-local resources that are safe to share across activity executions, such as pools, semaphores, caches, test counters, or service clients. Do not put workflow state here.

## Heartbeats and Cancellation

Use heartbeats for long-running activities:
- `ctx.record_heartbeat(...)` sends progress details.
- `ctx.heartbeat_details()` reads details from the last failed attempt.
- `ctx.is_cancelled()` and `ctx.cancelled().await` observe cancellation.

Local heartbeat anchor: `crates/sdk/examples/activity_heartbeating/workflows.rs:17`.

Cancellation is cooperative. For a cancellable long-running activity, heartbeat periodically and check cancellation between units of work. Avoid explicit sleeps in tests; production activities may wait for real external work.

## Errors

Activity return type is `Result<T, ActivityError>`.

Use application failures when callers need retry semantics:
- retryable failure with an `ApplicationFailure` builder and optional next retry delay
- non-retryable failure for permanent validation or business failures
- `ActivityError::cancelled()` for cancellation

Local API anchors:
- error types in SDK README: `crates/sdk/README.md:290`
- `ActivityContext::cancelled`: `crates/sdk/src/activities.rs:152`
- `ActivityContext::heartbeat_details`: `crates/sdk/src/activities.rs:163`
- `ActivityContext::record_heartbeat`: `crates/sdk/src/activities.rs:169`

## Payload Size and Side Effects

Official activity docs warn that returned payloads are recorded in workflow history and subject to payload limits. Keep activity outputs small, serializable, and meaningful. Store large data externally and return references.

Activities are the right place for nondeterministic work:
- network calls
- file I/O
- database operations
- system time
- random generation
- using a Temporal client

## Local Activities

Use local activities for short-lived side effects that should run on the same worker as the workflow. Anchor: `crates/sdk/README.md:298`.

Review local activity timeouts carefully because they trade server scheduling for worker-local execution.
