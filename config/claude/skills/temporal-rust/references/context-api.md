# Context API

The Temporal Rust SDK provides three context types for different handler scenarios, plus a base context for infrastructure.

## WorkflowContext<W>

The full async context used in `#[run]` methods and async signal/update handlers.

**Not Send or Sync** — workflows run in a `LocalSet` for deterministic execution.

### Info Methods

```rust
ctx.namespace()              // &str — workflow namespace
ctx.task_queue()             // &str — task queue name
ctx.workflow_time()          // Option<SystemTime> — deterministic current time
ctx.history_length()         // u32 — current history event count
ctx.is_replaying()           // bool — true during replay
ctx.random_seed()            // u64 — deterministic random seed
ctx.continue_as_new_suggested() // bool — server suggests continue-as-new
ctx.current_build_id()       // Option<&str> — worker build ID
ctx.current_deployment_version() // Option<&WorkerDeploymentVersion>
ctx.payload_converter()      // &dyn PayloadConverter
ctx.headers()                // &HashMap<String, Payload>
```

### State Access

```rust
// Immutable read (cheap, no side effects)
let value = ctx.state(|s| s.field.clone());

// Mutable access (drains wait_condition wakers)
ctx.state_mut(|s| {
    s.field = new_value;
});

// Reactive wait — suspends until predicate is true
// Wakers are checked after every state_mut call
ctx.wait_condition(|s| s.status == "ready").await;
```

### Activity Execution

```rust
use temporalio_sdk::workflow_context::ActivityOptions;

let opts = ActivityOptions {
    start_to_close_timeout: Some(Duration::from_secs(30)),
    ..Default::default()
};

// Type-safe activity call
let result = ctx.start_activity(MyActivities::process, input, opts).await?;

// Local activity (in-process, lower overhead)
let result = ctx.start_local_activity(MyActivities::quick_op, input, local_opts).await?;
```

### Timers

```rust
use temporalio_sdk::TimerResult;

// Await timer
match ctx.timer(Duration::from_secs(60)).await {
    TimerResult::Fired => { /* timer completed */ }
    TimerResult::Cancelled => { /* cancelled */ }
}
```

### Child Workflows

```rust
use temporalio_sdk::workflow_context::ChildWorkflowOptions;

let opts = ChildWorkflowOptions {
    workflow_id: "child-123".to_string(),
    workflow_type: "ChildType".to_string(),
    ..Default::default()
};

let result = ctx.child_workflow(opts, input).await?;
```

### External Signals and Cancellation

```rust
use temporalio_sdk::workflow_context::SignalWorkflowOptions;

// Signal another workflow
let opts = SignalWorkflowOptions {
    workflow_id: "target-wf".to_string(),
    signal_name: "my_signal".to_string(),
    ..Default::default()
};
ctx.signal_workflow(opts, signal_data).await?;

// Cancel another workflow
ctx.cancel_external(CancelExternalOptions {
    workflow_id: "target-wf".to_string(),
    ..Default::default()
}).await?;

// Detect own cancellation
ctx.cancelled().await;
```

### Search Attributes and Memo

```rust
ctx.search_attributes()  // current search attributes
ctx.upsert_search_attributes(new_attrs);
ctx.upsert_memo(new_memo);
```

### Versioning (Patching)

```rust
if ctx.patched("my-change-id") {
    // New code path
} else {
    // Old code path (for replay compatibility)
}

// After all old workflows complete:
ctx.deprecate_patch("my-change-id");
// Now only new code path runs
```

### Continue-As-New

```rust
ctx.continue_as_new(new_input)?;
```

## SyncWorkflowContext<W>

Used in synchronous signal and update handlers. Provides a subset of WorkflowContext.

```rust
#[signal]
pub fn handle_event(&mut self, ctx: &mut SyncWorkflowContext<Self>, event: Event) {
    // Available methods:
    ctx.namespace();
    ctx.task_queue();
    ctx.workflow_time();
    ctx.history_length();
    ctx.is_replaying();
    ctx.continue_as_new_suggested();
    ctx.headers();

    // Direct state mutation via &mut self
    self.events.push(event);
}
```

**Key difference from WorkflowContext**: No async operations. Cannot call activities, timers, or child workflows. Has direct `&mut self` access instead of `state()`/`state_mut()` closures.

## WorkflowContextView

Read-only context for `#[query]` handlers and `#[init]`.

```rust
#[query]
pub fn get_info(&self, ctx: &WorkflowContextView) -> WorkflowInfo {
    WorkflowInfo {
        workflow_id: ctx.workflow_id.clone(),
        run_id: ctx.run_id.clone(),
        workflow_type: ctx.workflow_type.clone(),
        task_queue: ctx.task_queue.clone(),
        namespace: ctx.namespace.clone(),
        attempt: ctx.attempt,
        start_time: ctx.start_time,
    }
}
```

### Available Fields

| Field | Type | Description |
|-------|------|-------------|
| `workflow_id` | `String` | Workflow ID |
| `run_id` | `String` | Current run ID |
| `workflow_type` | `String` | Workflow type name |
| `task_queue` | `String` | Task queue |
| `namespace` | `String` | Namespace |
| `attempt` | `u32` | Retry attempt number |
| `first_execution_run_id` | `String` | First run in chain |
| `continued_from_run_id` | `Option<String>` | Previous run (continue-as-new) |
| `start_time` | `Option<SystemTime>` | Workflow start time |
| `execution_timeout` | `Option<Duration>` | Max execution time |
| `run_timeout` | `Option<Duration>` | Max single run time |
| `task_timeout` | `Option<Duration>` | Max task processing time |
| `parent` | `Option<ParentWorkflowInfo>` | Parent workflow info |
| `root` | `Option<RootWorkflowInfo>` | Root workflow info |
| `retry_policy` | `Option<RetryPolicy>` | Applied retry policy |
| `cron_schedule` | `Option<String>` | Cron schedule if set |
| `memo` | `Option<Memo>` | Workflow memo |
| `search_attributes` | `Option<SearchAttributes>` | Search attributes |

## Command Pipeline

Workflow operations go through an internal command pipeline:

```
Workflow code issues command (activity, timer, etc.)
    ↓
CancellableWFCommandFut created (implements Future)
    ↓
Command buffered to internal channel
    ↓
Workflow task yields
    ↓
Worker sends commands to Temporal server
    ↓
Server processes and returns result
    ↓
WorkflowActivation dispatches result
    ↓
Future resolved with UnblockEvent
    ↓
Workflow continues execution
```

All command futures are cancellable — dropping the future cancels the operation.
