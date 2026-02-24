# Code Review Checklist

Use this checklist when reviewing Temporal Rust code for correctness, production-readiness, and best practices.

## Critical: Determinism Violations

These will cause nondeterminism errors during replay and break running workflows.

- [ ] **No wall-clock time in workflows** — `SystemTime::now()`, `Instant::now()` → use `ctx.workflow_time()`
- [ ] **No random in workflows** — `rand::random()`, `Uuid::new_v4()` → use `ctx.random_seed()`
- [ ] **No sleeping in workflows** — `thread::sleep()`, `tokio::time::sleep()` → use `ctx.timer()`
- [ ] **No I/O in workflows** — file, network, database → move to activities
- [ ] **No HashMap iteration for commands** — use `BTreeMap` or sort before iterating
- [ ] **No env vars for branching** — `std::env::var()` → use `ctx.patched()` or workflow input
- [ ] **No tokio::spawn in workflows** — use workflow-context async patterns
- [ ] **No external crate calls with side effects** — anything that touches the outside world belongs in an activity

## High Priority: Error Handling

- [ ] **Activities distinguish retryable vs non-retryable errors** — transient failures should be `Retryable`, permanent failures should be `NonRetryable`
- [ ] **Retry policies are explicit** — don't rely on defaults for production; set `maximum_attempts`, `initial_interval`, `backoff_coefficient`
- [ ] **Non-retryable error types listed** — `RetryPolicy.non_retryable_error_types` prevents wasted retries on known-permanent failures
- [ ] **Workflow error handling is complete** — `ActExitValue::Err` and `ActExitValue::Panic` cases handled
- [ ] **No unwrap/expect in workflows** — panics in workflows cause task failure; use `?` or explicit error handling
- [ ] **No unwrap/expect in activities** — use `ActivityError` variants; panics waste retry attempts

## High Priority: Timeouts

- [ ] **Activities have timeouts** — at minimum `start_to_close_timeout`; long-running need `heartbeat_timeout`
- [ ] **Child workflows have timeouts** — `execution_timeout` and/or `run_timeout`
- [ ] **Timeouts are realistic** — not too short (false failures) or too long (resource waste)

## High Priority: Heartbeats

- [ ] **Long-running activities heartbeat** — any activity > 30s should call `record_heartbeat()`
- [ ] **Heartbeat details enable resume** — save progress so retries skip completed work
- [ ] **Heartbeat frequency reasonable** — not too frequent (overhead) or too sparse (late cancellation detection)
- [ ] **Heartbeat details are recoverable** — `heartbeat_details()` checked on retry start

## Medium Priority: Cancellation

- [ ] **Activities check cancellation** — `ctx.is_cancelled()` or `ctx.cancelled().await`
- [ ] **Workflow handles cancellation** — `ctx.cancelled()` for cleanup logic
- [ ] **Cancellation cleanup is bounded** — cleanup shouldn't take longer than the original operation
- [ ] **CancellationType appropriate** — `TryCancel` vs `WaitCancellationCompleted` vs `Abandon`

## Medium Priority: State Management

- [ ] **state() for reads, state_mut() for writes** — unnecessary `state_mut()` drains wakers
- [ ] **wait_condition predicates are sound** — will eventually become true after relevant state_mut calls
- [ ] **No deadlocks** — `wait_condition` isn't waiting on something that can never happen
- [ ] **Workflow state is serializable** — all fields survive serialization for continue-as-new

## Medium Priority: Signals, Queries, Updates

- [ ] **Signal handlers don't block** — sync signals should be fast; use async signals for activity calls
- [ ] **Query handlers are pure** — no state mutation in `#[query]` handlers
- [ ] **Update validators are cheap** — validation runs before the update, should be fast
- [ ] **Update handlers return meaningful errors** — don't swallow errors

## Medium Priority: Configuration

- [ ] **WorkerOptions tuned** — `max_cached_workflows`, poller behavior appropriate for workload
- [ ] **Task queue names are consistent** — workflow and worker use the same queue
- [ ] **Namespace is correct** — especially for Temporal Cloud deployments
- [ ] **Worker versioning configured** — `deployment_options` set for production workers

## Low Priority: Code Quality

- [ ] **Types implement required traits** — `TemporalSerializable` / `TemporalDeserializable` for I/O types
- [ ] **Activity names are stable** — renaming breaks running workflows; use `name = "..."` to decouple
- [ ] **Workflow names are stable** — same as activities
- [ ] **No unnecessary cloning** — use references where possible in state access closures
- [ ] **Logging uses replay guard** — `if !ctx.is_replaying() { ... }` for log statements

## Production Readiness

- [ ] **Graceful shutdown** — `worker.shutdown_handle()` wired to signal handler
- [ ] **Connection resilience** — client handles reconnection
- [ ] **Metrics/telemetry** — `TelemetryOptions` configured for observability
- [ ] **Search attributes** — key workflow state is queryable via search attributes
- [ ] **Continue-as-new** — long-running workflows check `continue_as_new_suggested()`
- [ ] **Versioning strategy** — `patched()` used for workflow logic changes
- [ ] **Interceptors** — `FailOnNondeterminismInterceptor` in dev/staging

## Anti-Patterns

### 1. Activity Inside Query Handler

```rust
// BAD — queries are read-only and synchronous
#[query]
pub fn get_data(&self, ctx: &WorkflowContextView) -> String {
    // Cannot call activities here
}
```

### 2. Blocking Sync Signal

```rust
// BAD — blocks the workflow task
#[signal]
pub fn handle(&mut self, ctx: &mut SyncWorkflowContext<Self>, data: String) {
    std::thread::sleep(Duration::from_secs(5)); // BLOCKS!
}
```

### 3. Ignoring Replay in Metrics

```rust
// BAD — metrics double-counted during replay
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<()> {
    metrics::counter!("workflow_started").increment(1); // fires on every replay!
}

// GOOD
if !ctx.is_replaying() {
    metrics::counter!("workflow_started").increment(1);
}
```

### 4. Unbounded History Growth

```rust
// BAD — history grows forever
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<()> {
    loop {
        ctx.start_activity(MyActivities::poll, (), opts).await?;
        ctx.timer(Duration::from_secs(60)).await;
        // History grows with each iteration!
    }
}

// GOOD — use continue-as-new
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<()> {
    loop {
        ctx.start_activity(MyActivities::poll, (), opts).await?;
        ctx.timer(Duration::from_secs(60)).await;

        if ctx.continue_as_new_suggested() {
            ctx.continue_as_new(())?;
            return Ok(());
        }
    }
}
```
