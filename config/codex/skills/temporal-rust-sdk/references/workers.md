# Workers

Use this for worker processes, task queues, type registration, runtime/client wiring, worker options, shutdown, and tuning.

Official docs:
- Worker processes: https://docs.temporal.io/develop/rust/workers/worker-process
- Quickstart worker flow: https://docs.temporal.io/develop/rust/quickstart

Local anchors:
- Hello world worker: `crates/sdk/examples/hello_world/worker.rs:1`
- Worker options: `crates/sdk/src/lib.rs:182`
- Worker registration helpers: `crates/sdk/src/lib.rs:287`
- `Worker::new`: `crates/sdk/src/lib.rs:468`
- `Worker::run`: `crates/sdk/src/lib.rs:593`
- Activity-only worker doc example: `crates/sdk/src/lib.rs:9`
- Worker config notes in SDK README: `crates/sdk/README.md:331`

## Worker Process Model

Official worker docs describe a Worker Process as the process where workflow and activity code executes. A worker polls one task queue and reports results to Temporal.

Important registration rules:
- Each Worker Entity must register the exact Workflow Types and Activity Types it may execute.
- Each Worker Entity is associated with exactly one task queue.
- Workers polling the same task queue should register the same workflow and activity types.

## Runtime, Client, Worker

The common local shape is:

```rust
let runtime = CoreRuntime::new_assume_tokio(
    RuntimeOptions::builder()
        .telemetry_options(TelemetryOptions::builder().build())
        .build()?,
)?;

let (conn_opts, client_opts) =
    ClientOptions::load_from_config(LoadClientConfigProfileOptions::default())?;
let connection = Connection::connect(conn_opts).await?;
let client = Client::new(connection, client_opts)?;

let worker_options = WorkerOptions::new("hello-world")
    .register_workflow::<HelloWorldWorkflow>()
    .register_activities(GreetingActivities)
    .build();

let mut worker = Worker::new(&runtime, client, worker_options)?;
worker.run().await?;
```

Source: `crates/sdk/examples/hello_world/worker.rs:13`.

## WorkerOptions

Start at `crates/sdk/src/lib.rs:182` for exact fields. Common knobs include:
- `task_queue`
- `deployment_options`
- `client_identity_override`
- `max_cached_workflows`
- `tuner`
- workflow/activity/nexus poller behavior
- `task_types`
- heartbeat throttle intervals
- per-task-queue and per-worker activity rate limits
- workflow failure error policies
- `graceful_shutdown_period`
- `detect_nondeterministic_futures`

Use the builder where possible:

```rust
let worker_options = WorkerOptions::new("task-queue")
    .register_activities(my_activities)
    .register_workflow::<MyWorkflow>()
    .build();
```

For activity-only workers, set task types explicitly. Anchor: `crates/sdk/src/lib.rs:50`.

## Registration

Prefer registering via `WorkerOptions` at construction time:
- `.register_workflow::<MyWorkflow>()`
- `.register_activities(MyActivities)`
- `.register_activity::<SpecificActivity>(Arc::new(...))` for one activity

Late registration methods exist on `Worker` too, but construction-time registration is easier to reason about and matches examples.

Use `register_workflow_with_factory` only for advanced cases that need un-serializable injected state. The local docs warn this can easily cause nondeterminism: `crates/sdk/src/lib.rs:309`.

## Shutdown

`Worker::run()` resolves after explicit shutdown or unrecoverable error. If a task needs a shutdown path while `run()` holds `&mut self`, use `shutdown_handle()` from `crates/sdk/src/lib.rs:544`.

For tests, prefer harness helpers that drain and shut down workers cleanly instead of sleeping.

## Review Checks

- Does the worker poll the same task queue used by workflow starts?
- Do all workers on a task queue register the same types?
- Is the client namespace/config correct for local, CI, or Cloud?
- Are activities and workflows registered on the right worker process?
- Is `detect_nondeterministic_futures` left enabled unless there is a documented migration reason?
