# Determinism Rules

Temporal workflows must be deterministic — the same input must always produce the same sequence of commands. This is because workflows are replayed from history to rebuild state after restarts.

## Forbidden in Workflows

| Operation | Why | Alternative |
|-----------|-----|-------------|
| `SystemTime::now()` | Non-deterministic | `ctx.workflow_time()` |
| `Instant::now()` | Non-deterministic | `ctx.workflow_time()` |
| `rand::random()` | Non-deterministic | `ctx.random_seed()` + seeded RNG |
| `std::thread::sleep()` | Blocks executor | `ctx.timer(duration).await` |
| `tokio::time::sleep()` | Not replay-safe | `ctx.timer(duration).await` |
| `tokio::fs::*` / `std::fs::*` | Side effect | Move to an activity |
| `reqwest::get()` / HTTP | Side effect | Move to an activity |
| `sqlx::query()` / DB | Side effect | Move to an activity |
| `std::env::var()` | Non-deterministic | Pass as workflow input or use search attributes |
| `HashMap` iteration | Non-deterministic order | Use `BTreeMap` or `Vec` |
| `Uuid::new_v4()` | Non-deterministic | Use `ctx.random_seed()` or pass from activity |
| Spawning OS threads | Side effect | Use workflow primitives |
| `tokio::spawn()` | Not tracked by Temporal | Use workflow-context async patterns |

## Safe Operations in Workflows

| Operation | Notes |
|-----------|-------|
| `ctx.workflow_time()` | Deterministic timestamp |
| `ctx.timer(d).await` | Durable, replay-safe timer |
| `ctx.start_activity(...)` | Replay-safe activity call |
| `ctx.start_local_activity(...)` | Replay-safe local activity |
| `ctx.child_workflow(...)` | Replay-safe child workflow |
| `ctx.state()` / `ctx.state_mut()` | State access |
| `ctx.wait_condition(pred)` | Reactive state wait |
| `ctx.is_replaying()` | Check if replaying |
| Pure computation | Math, string ops, struct creation |
| Logging (with replay guard) | `if !ctx.is_replaying() { log!(...) }` |

## Replay and is_replaying()

During replay, Temporal re-executes the workflow code but matches commands against history instead of actually executing them. Use `is_replaying()` to skip side effects:

```rust
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<()> {
    if !ctx.is_replaying() {
        // Only log on real execution, not during replay
        tracing::info!("Starting workflow");
    }

    // This is safe — during replay, it matches against history
    let result = ctx.start_activity(MyActivities::process, input, opts).await?;

    Ok(())
}
```

## Versioning with patched() / deprecate_patch()

When you need to change workflow logic for existing running workflows:

### Step 1: Add patch (both old and new code)

```rust
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<()> {
    if ctx.patched("new-validation-v2") {
        // New code path
        let result = ctx.start_activity(MyActivities::validate_v2, input, opts).await?;
    } else {
        // Old code path (for workflows started before this change)
        let result = ctx.start_activity(MyActivities::validate_v1, input, opts).await?;
    }
    Ok(())
}
```

### Step 2: After all old workflows complete, deprecate

```rust
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<()> {
    ctx.deprecate_patch("new-validation-v2");
    // Only new code path remains
    let result = ctx.start_activity(MyActivities::validate_v2, input, opts).await?;
    Ok(())
}
```

### Step 3: Eventually remove the deprecate_patch call entirely

## Common Determinism Pitfalls

### 1. Conditional Logic on External State

```rust
// BAD — environment can change between replays
if std::env::var("FEATURE_FLAG").is_ok() {
    do_new_thing();
}

// GOOD — use patched() for versioning
if ctx.patched("feature-flag-v2") {
    do_new_thing();
}
```

### 2. Collection Ordering

```rust
// BAD — HashMap iteration order is non-deterministic
let map: HashMap<String, i32> = get_data();
for (k, v) in &map {
    ctx.start_activity(MyActivities::process, (k.clone(), *v), opts).await?;
}

// GOOD — sort first or use BTreeMap
let mut items: Vec<_> = map.into_iter().collect();
items.sort_by_key(|(k, _)| k.clone());
for (k, v) in items {
    ctx.start_activity(MyActivities::process, (k, v), opts).await?;
}
```

### 3. Non-Deterministic Random

```rust
// BAD
let id = uuid::Uuid::new_v4().to_string();

// GOOD — use workflow's deterministic seed
let seed = ctx.random_seed();
let mut rng = rand::rngs::StdRng::seed_from_u64(seed);
let id: u64 = rng.gen();
```

### 4. Time-Based Logic

```rust
// BAD
let now = SystemTime::now();

// GOOD
let now = ctx.workflow_time().expect("workflow time available");
```

## Nondeterminism Detection

Use `FailOnNondeterminismInterceptor` during development/testing to catch issues early:

```rust
use temporalio_sdk::interceptors::FailOnNondeterminismInterceptor;

worker.set_worker_interceptor(FailOnNondeterminismInterceptor {});
```

This causes the worker to exit immediately if a nondeterminism error is detected during replay, rather than silently continuing with potentially incorrect state.
