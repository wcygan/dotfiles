# Workflow Patterns

## Defining a Workflow

A workflow is a struct + impl block annotated with proc macros. The struct holds state that persists across replays.

```rust
use temporalio_macros::{workflow, workflow_methods};
use temporalio_sdk::{WorkflowContext, WorkflowContextView, SyncWorkflowContext, WorkflowResult};

#[workflow]
pub struct OrderWorkflow {
    status: String,
    items: Vec<String>,
}

#[workflow_methods]
impl OrderWorkflow {
    #[init]
    pub fn new(ctx: &WorkflowContextView, items: Vec<String>) -> Self {
        Self {
            status: "pending".to_string(),
            items,
        }
    }

    #[run]
    pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<String> {
        // Orchestration logic here
        let item_count = ctx.state(|s| s.items.len());
        Ok(format!("Processed {} items", item_count))
    }
}
```

### Macro Attributes

- `#[workflow]` — optional `name = "CustomName"` override (defaults to struct name)
- `#[workflow_methods]` — generates `WorkflowImplementation` and handler traits
- `#[init]` — receives `&WorkflowContextView` + optional input; called before `#[run]`
- `#[run]` — receives `&mut WorkflowContext<Self>` + optional input; the main entry point

## State Management

Workflow state lives in the struct fields. Access via context closures:

```rust
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<String> {
    // Read-only access (no waker drain)
    let count = ctx.state(|s| s.items.len());

    // Mutable access (drains wakers from wait_condition)
    ctx.state_mut(|s| {
        s.status = "processing".to_string();
    });

    // Wait for state change (reactive pattern)
    ctx.wait_condition(|s| s.status == "approved").await;

    Ok(ctx.state(|s| s.status.clone()))
}
```

**Important**: `state()` is cheap; `state_mut()` drains pending wakers. Use `state()` for reads.

## Signals (Fire-and-Forget Inbound Events)

### Sync Signal (most common)

```rust
#[signal]
pub fn add_item(&mut self, ctx: &mut SyncWorkflowContext<Self>, item: String) {
    self.items.push(item);
}
```

- Direct `&mut self` access — no closure needed
- Executes synchronously before the next workflow task
- Cannot call async operations

### Async Signal

```rust
#[signal]
pub async fn process_item(ctx: WorkflowContext<Self>, item: String) {
    let result = ctx.start_activity(
        MyActivities::process,
        item,
        ActivityOptions {
            start_to_close_timeout: Some(Duration::from_secs(30)),
            ..Default::default()
        },
    ).await;
    // Handle result...
}
```

- Uses `WorkflowContext<Self>` (not `&mut self`)
- Can call activities, timers, child workflows
- State access via `ctx.state()` / `ctx.state_mut()`

## Queries (Read-Only Inspection)

```rust
#[query]
pub fn get_status(&self, ctx: &WorkflowContextView) -> String {
    self.status.clone()
}

#[query]
pub fn get_items(&self, ctx: &WorkflowContextView) -> Vec<String> {
    self.items.clone()
}
```

- Always synchronous, always `&self` (immutable)
- Must not modify state
- `WorkflowContextView` provides read-only workflow metadata

## Updates (Request-Response with Validation)

### Sync Update

```rust
#[update(name = "approve_order")]
pub fn approve(&mut self, ctx: &mut SyncWorkflowContext<Self>) -> Result<String, String> {
    if self.status != "pending" {
        return Err(format!("Cannot approve: status is {}", self.status));
    }
    self.status = "approved".to_string();
    Ok(self.status.clone())
}

#[update_validator(approve)]
pub fn validate_approve(&self, ctx: &WorkflowContextView) -> Result<(), String> {
    if self.items.is_empty() {
        return Err("Cannot approve empty order".to_string());
    }
    Ok(())
}
```

### Async Update

```rust
#[update]
pub async fn fulfill(ctx: WorkflowContext<Self>) -> Result<String, anyhow::Error> {
    let result = ctx.start_activity(
        MyActivities::ship_order,
        ctx.state(|s| s.items.clone()),
        ActivityOptions {
            start_to_close_timeout: Some(Duration::from_secs(300)),
            ..Default::default()
        },
    ).await?;
    ctx.state_mut(|s| s.status = "fulfilled".to_string());
    Ok(result)
}
```

- Validators run before the update handler
- Validators are always sync and `&self`
- `#[update_validator(handler_name)]` links validator to its update

## Calling Activities from Workflows

```rust
use temporalio_sdk::workflow_context::ActivityOptions;

#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<String> {
    let opts = ActivityOptions {
        start_to_close_timeout: Some(Duration::from_secs(30)),
        schedule_to_close_timeout: Some(Duration::from_secs(60)),
        retry_policy: Some(RetryPolicy {
            initial_interval: Duration::from_secs(1),
            backoff_coefficient: 2.0,
            maximum_attempts: 3,
            ..Default::default()
        }),
        ..Default::default()
    };

    let result = ctx.start_activity(MyActivities::process, "input".to_string(), opts)
        .await
        .map_err(|e| anyhow::anyhow!("Activity failed: {e}"))?;

    Ok(result)
}
```

## Timers

```rust
use temporalio_sdk::TimerResult;

// Simple timer
match ctx.timer(Duration::from_secs(300)).await {
    TimerResult::Fired => { /* timer completed */ }
    TimerResult::Cancelled => { /* workflow or timer was cancelled */ }
}

// Cancellable timer (store the future, cancel later)
let timer_fut = ctx.timer(Duration::from_hours(24));
// Cancel with: timer_fut.cancel();
```

## Child Workflows

```rust
use temporalio_sdk::workflow_context::ChildWorkflowOptions;

let child_opts = ChildWorkflowOptions {
    workflow_id: format!("child-{}", order_id),
    workflow_type: "PaymentWorkflow".to_string(),
    task_queue: Some("payments".to_string()),
    execution_timeout: Some(Duration::from_secs(3600)),
    parent_close_policy: ParentClosePolicy::Terminate,
    ..Default::default()
};

let result = ctx.child_workflow(child_opts, payment_input).await?;
```

## Continue-As-New

```rust
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<()> {
    loop {
        // Process batch...

        if ctx.continue_as_new_suggested() {
            // Re-run with fresh history
            ctx.continue_as_new(next_batch_input)?;
            return Ok(());
        }
    }
}
```

## Cancellation

```rust
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<String> {
    tokio::select! {
        result = do_work(ctx) => result,
        _ = ctx.cancelled() => {
            // Cleanup logic
            Ok("cancelled".to_string())
        }
    }
}
```
