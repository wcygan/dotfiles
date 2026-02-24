---
name: temporal-rust
description: Temporal Rust SDK expert for durable workflow orchestration. Auto-loads when working with Temporal workflows, activities, workers in Rust. Covers #[workflow], #[activity], #[workflow_methods], WorkflowContext, ActivityContext, temporalio-sdk, temporalio-macros, temporalio-client, Worker, WorkerOptions, task queues, signals, queries, updates, timers, child workflows, heartbeats, retry policies, cancellation, determinism, replay safety, interceptors, data conversion, and testing patterns. Also provides code review for determinism violations and test generation for Temporal Rust code. Keywords: temporal, rust, workflow, activity, durable execution, temporalio-sdk, temporal rust sdk.
---

# Temporal Rust SDK

Temporal is a durable execution platform. Workflows are async Rust functions that survive process restarts; activities are the side-effecting work units. The Rust SDK uses proc macros (`#[workflow]`, `#[activity]`) for ergonomic definitions.

**Status**: Alpha (v0.1.0-alpha.1). Activity-only workers are the most stable surface; workflow API is evolving.

**Docs**: <https://docs.rs/temporalio-sdk/latest/temporalio_sdk/>

## Crate Map

| Crate | Purpose |
|-------|---------|
| `temporalio-sdk` | Main SDK — Worker, contexts, registration |
| `temporalio-macros` | Proc macros — `#[workflow]`, `#[activity]`, etc. |
| `temporalio-client` | gRPC client — Connection, Client, ClientOptions |
| `temporalio-common` | Shared types — payloads, retry policies, data converters |
| `temporalio-sdk-core` | Core runtime — RuntimeOptions, CoreRuntime, Url |

## Core API Quick Reference

### Workflow Macros (`temporalio_macros`)

| Macro | Purpose |
|-------|---------|
| `#[workflow]` | Mark struct as a workflow (optional `name = "..."`) |
| `#[workflow_methods]` | Generate trait impls on the impl block |
| `#[init]` | Optional constructor receiving `&WorkflowContextView` |
| `#[run]` | Required async entry point — `&mut WorkflowContext<Self>` |
| `#[signal]` | Signal handler — sync (`&mut self, &mut SyncWorkflowContext`) or async |
| `#[query]` | Read-only query — `&self, &WorkflowContextView` |
| `#[update]` | State-mutating update — sync or async, returns `Result` |
| `#[update_validator(handler)]` | Validation hook for an `#[update]` |

### Activity Macros

| Macro | Purpose |
|-------|---------|
| `#[activities]` | Mark impl block as activity definitions |
| `#[activity]` | Mark method as an activity (optional `name = "..."`) |

### WorkflowContext Methods

| Category | Key Methods |
|----------|-------------|
| **Info** | `namespace()`, `task_queue()`, `workflow_time()`, `is_replaying()`, `history_length()` |
| **Activities** | `start_activity(fn, input, opts)`, `start_local_activity(fn, input, opts)` |
| **Timers** | `timer(duration)` → `CancellableFuture<TimerResult>` |
| **Children** | `child_workflow(opts, input)` |
| **Signals** | `signal_workflow(opts, input)` |
| **Cancel** | `cancelled()`, `cancel_external(opts)` |
| **State** | `state(\|s\| ...)`, `state_mut(\|s\| ...)`, `wait_condition(pred)` |
| **Search** | `search_attributes()`, `upsert_search_attributes()`, `upsert_memo()` |
| **Versioning** | `patched(id)`, `deprecate_patch(id)`, `current_deployment_version()` |

### ActivityContext Methods

| Method | Purpose |
|--------|---------|
| `info()` | Activity metadata (task token, attempt, timeouts) |
| `record_heartbeat(details)` | Send heartbeat to server |
| `is_cancelled()` / `cancelled()` | Check/await cancellation |
| `heartbeat_details()` | Recover details from previous attempt |
| `headers()` | Access activity headers |

### Worker Setup

| API | Purpose |
|-----|---------|
| `Worker::new(&runtime, client, options)` | Create worker |
| `worker.run().await` | Start polling (blocks until shutdown) |
| `worker.shutdown_handle()` | Get shutdown closure |
| `worker.set_worker_interceptor(impl)` | Add interceptor |
| `WorkerOptions::new(task_queue)` | Builder entry point |

## Architecture

```
Application Code
      │  ExecuteWorkflow / SignalWorkflow / QueryWorkflow
      ▼
┌─────────────────────┐
│  temporalio-client   │  gRPC connection to Temporal
└────────┬────────────┘
         │  gRPC
         ▼
┌─────────────────────┐
│  Temporal Server     │  localhost:7233 / Temporal Cloud
└────────┬────────────┘
         │  Task Queue polling
         ▼
┌─────────────────────┐
│  Worker              │  temporalio-sdk
│  (Hosts Workflows    │  Runs in tokio + LocalSet
│   & Activities)      │  Workflows are !Send (deterministic)
└─────────────────────┘
```

## Code Review Mode

When reviewing Temporal Rust code, check for:
1. **Determinism violations** — no `SystemTime::now()`, `rand`, `std::thread::sleep`, or raw I/O in workflows
2. **Missing heartbeats** — long-running activities without `record_heartbeat()`
3. **Timeout gaps** — activities without `start_to_close_timeout` or `schedule_to_close_timeout`
4. **Error type misuse** — using `anyhow!` where `ActivityError::NonRetryable` is needed
5. **State access** — using `state_mut` when `state` suffices (unnecessary waker drain)
6. **Cancellation ignorance** — activities that never check `is_cancelled()`

## References

- [Workflow Patterns](references/workflow-patterns.md) — defining workflows, init, run, signals, queries, updates, state management
- [Activity Patterns](references/activity-patterns.md) — defining activities, shared state, heartbeats, cancellation, error types
- [Worker Setup](references/worker-setup.md) — runtime, connection, client, worker configuration, registration
- [Context API](references/context-api.md) — WorkflowContext, SyncWorkflowContext, WorkflowContextView, command pipeline
- [Error Handling](references/error-handling.md) — WorkflowError, ActivityError, WorkflowTermination, result types
- [Determinism Rules](references/determinism-rules.md) — replay safety, forbidden operations, versioning, patching
- [Testing Patterns](references/testing-patterns.md) — interceptors, workflow replay, activity testing
- [Code Review Checklist](references/code-review-checklist.md) — common anti-patterns, determinism audit, production readiness
