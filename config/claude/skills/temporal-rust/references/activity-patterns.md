# Activity Patterns

Activities are the side-effecting work units in Temporal. They can fail, retry, heartbeat, and be distributed across workers.

## Defining Activities

```rust
use temporalio_macros::activities;
use temporalio_sdk::activities::{ActivityContext, ActivityError};

struct MyActivities;

#[activities]
impl MyActivities {
    #[activity]
    pub async fn send_email(
        _ctx: ActivityContext,
        to: String,
        body: String,
    ) -> Result<(), ActivityError> {
        // Real side-effecting work here
        Ok(())
    }

    #[activity(name = "custom_name")]
    pub async fn process(
        _ctx: ActivityContext,
        data: Vec<u8>,
    ) -> Result<String, ActivityError> {
        Ok(String::from_utf8_lossy(&data).to_string())
    }
}
```

### Key Rules

- Methods must be `async` and return `Result<T, ActivityError>`
- First parameter is always `ActivityContext`
- Use `name = "..."` to override the activity name (defaults to method name)
- Input/output types must implement `TemporalSerializable` / `TemporalDeserializable`

## Shared State (Arc<Self>)

Activities can hold shared state by taking `self: Arc<Self>`:

```rust
struct DbActivities {
    pool: sqlx::PgPool,
}

#[activities]
impl DbActivities {
    #[activity]
    pub async fn fetch_user(
        self: Arc<Self>,
        ctx: ActivityContext,
        user_id: i64,
    ) -> Result<User, ActivityError> {
        let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", user_id)
            .fetch_one(&self.pool)
            .await
            .map_err(|e| ActivityError::from(anyhow::anyhow!(e)))?;
        Ok(user)
    }
}

// Registration passes the Arc instance
let db_activities = Arc::new(DbActivities { pool });
worker_options.register_activities(db_activities);
```

## Heartbeats

Long-running activities should heartbeat to:
1. Report progress to the server
2. Detect cancellation
3. Enable retry from last checkpoint

```rust
#[activity]
pub async fn process_large_file(
    ctx: ActivityContext,
    file_path: String,
) -> Result<u64, ActivityError> {
    let mut processed = 0u64;

    // Recover from previous attempt
    if let Some(details) = ctx.heartbeat_details().first() {
        processed = serde_json::from_slice(details.data.as_slice())
            .unwrap_or(0);
    }

    let file = tokio::fs::File::open(&file_path).await
        .map_err(|e| ActivityError::from(anyhow::anyhow!(e)))?;

    loop {
        // Process chunk...
        processed += chunk_size;

        // Heartbeat with progress
        let details = serde_json::to_vec(&processed).unwrap();
        ctx.record_heartbeat(vec![Payload {
            metadata: Default::default(),
            data: details.into(),
        }]);

        // Check cancellation
        if ctx.is_cancelled() {
            return Err(ActivityError::Cancelled { details: None });
        }

        if done {
            break;
        }
    }

    Ok(processed)
}
```

### Heartbeat Throttling

The worker automatically throttles heartbeats. Configure via `WorkerOptions`:
- `max_heartbeat_throttle_interval` — max time between server heartbeats (default 60s)
- `default_heartbeat_throttle_interval` — default throttle (default 30s)

## Cancellation

```rust
#[activity]
pub async fn cancellable_work(
    ctx: ActivityContext,
    input: String,
) -> Result<String, ActivityError> {
    tokio::select! {
        result = do_actual_work(&input) => {
            result.map_err(|e| ActivityError::from(anyhow::anyhow!(e)))
        }
        _ = ctx.cancelled() => {
            // Cleanup
            Err(ActivityError::Cancelled { details: None })
        }
    }
}
```

## ActivityError Types

```rust
// Retryable (default) — Temporal will retry per the retry policy
Err(ActivityError::Retryable {
    source: Box::new(anyhow::anyhow!("Transient network error")),
    explicit_delay: None, // or Some(Duration) to override backoff
})

// Shorthand for retryable
Err(ActivityError::from(anyhow::anyhow!("Will be retried")))

// Non-retryable — fails the activity immediately
Err(ActivityError::NonRetryable(
    Box::new(anyhow::anyhow!("Invalid input, don't retry"))
))

// Cancelled — activity was cancelled
Err(ActivityError::Cancelled { details: None })

// Async completion — activity will be completed externally via task token
Err(ActivityError::WillCompleteAsync)
```

## Local Activities

Execute in the same process as the workflow, with lower overhead:

```rust
use temporalio_sdk::workflow_context::LocalActivityOptions;

let opts = LocalActivityOptions {
    start_to_close_timeout: Some(Duration::from_secs(5)),
    retry_policy: Some(RetryPolicy {
        maximum_attempts: 3,
        ..Default::default()
    }),
    ..Default::default()
};

let result = ctx.start_local_activity(MyActivities::quick_check, input, opts).await?;
```

**When to use local activities:**
- Short operations (< 10s)
- No need for separate task queue routing
- Want to avoid network round-trip for scheduling

## ActivityInfo Fields

Available via `ctx.info()`:

| Field | Type | Description |
|-------|------|-------------|
| `task_token` | `Vec<u8>` | Token for async completion |
| `activity_id` | `String` | Unique ID within workflow |
| `activity_type` | `String` | Activity name |
| `task_queue` | `String` | Queue this ran on |
| `attempt` | `u32` | Current attempt number (starts at 1) |
| `heartbeat_timeout` | `Option<Duration>` | Max time between heartbeats |
| `scheduled_time` | `Option<SystemTime>` | When activity was scheduled |
| `started_time` | `Option<SystemTime>` | When this attempt started |
| `deadline` | `Option<SystemTime>` | When this attempt must complete |
| `workflow_type` | `String` | Parent workflow's type name |
| `workflow_namespace` | `String` | Parent workflow's namespace |
| `is_local` | `bool` | Whether this is a local activity |
| `retry_policy` | `Option<RetryPolicy>` | Applied retry policy |
