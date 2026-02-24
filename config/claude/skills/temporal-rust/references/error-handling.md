# Error Handling

## Workflow Errors

### WorkflowError

```rust
pub enum WorkflowError {
    PayloadConversion(PayloadConversionError),  // Serialization failure
    Execution(anyhow::Error),                   // Workflow logic failure
}
```

### WorkflowResult

```rust
pub type WorkflowResult<T> = Result<T, anyhow::Error>;

// Usage in #[run]
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<String> {
    Ok("done".to_string())
}
```

### WorkflowTermination

Non-normal workflow endings:

```rust
pub enum WorkflowTermination {
    Completed(Payload),       // Normal completion
    Failed(Failure),          // Workflow failed
    ContinuedAsNew(Payload),  // Restarted with new input
    Cancelled(Failure),       // Workflow was cancelled
    Evicted,                  // Evicted from worker cache
}
```

## Activity Errors

### ActivityError

```rust
pub enum ActivityError {
    // Will be retried per retry policy
    Retryable {
        source: Box<dyn std::error::Error + Send + Sync>,
        explicit_delay: Option<Duration>,  // Override retry backoff
    },

    // Cancelled by workflow or server
    Cancelled {
        details: Option<Payload>,
    },

    // Fails immediately, no retry
    NonRetryable(Box<dyn std::error::Error + Send + Sync>),

    // Activity will be completed externally
    WillCompleteAsync,
}
```

### Choosing the Right Error Type

| Scenario | Error Type | Example |
|----------|------------|---------|
| Transient network failure | `Retryable` | HTTP 503, connection timeout |
| Invalid input | `NonRetryable` | Bad email format, missing field |
| Rate limited | `Retryable` with `explicit_delay` | API 429 with Retry-After |
| User requested cancel | `Cancelled` | Workflow cancelled the activity |
| External completion | `WillCompleteAsync` | Waiting for human approval |

### Creating ActivityError

```rust
// From anyhow (defaults to Retryable)
let err = ActivityError::from(anyhow::anyhow!("transient failure"));

// Explicit retryable with delay
let err = ActivityError::Retryable {
    source: Box::new(anyhow::anyhow!("rate limited")),
    explicit_delay: Some(Duration::from_secs(30)),
};

// Non-retryable
let err = ActivityError::NonRetryable(
    Box::new(anyhow::anyhow!("invalid input: {}", reason))
);

// Cancelled
let err = ActivityError::Cancelled { details: None };
```

## Activity Execution Results (in Workflows)

When a workflow calls an activity, the result type is:

```rust
pub enum ActExitValue<T> {
    Ok(T),          // Activity completed successfully
    Err(Failure),   // Activity failed (after all retries)
    Panic(String),  // Activity panicked
}
```

## Timer Results

```rust
pub enum TimerResult {
    Fired,      // Timer completed normally
    Cancelled,  // Timer was cancelled
}
```

## External Workflow Results

```rust
pub type SignalExternalWfResult = Result<SignalExternalOk, Failure>;
pub type CancelExternalWfResult = Result<CancelExternalOk, Failure>;
```

## Payload Conversion Errors

```rust
pub struct PayloadConversionError {
    // Serialization/deserialization failures
    // Occurs when input/output types can't be converted
}
```

## Error Handling Patterns

### Activity with Comprehensive Error Handling

```rust
#[activity]
pub async fn process_payment(
    ctx: ActivityContext,
    payment: PaymentRequest,
) -> Result<PaymentResult, ActivityError> {
    // Validate input (non-retryable)
    if payment.amount <= 0 {
        return Err(ActivityError::NonRetryable(
            Box::new(anyhow::anyhow!("Invalid amount: {}", payment.amount))
        ));
    }

    // Check cancellation before expensive work
    if ctx.is_cancelled() {
        return Err(ActivityError::Cancelled { details: None });
    }

    // Attempt the work (retryable on failure)
    match payment_gateway::charge(&payment).await {
        Ok(result) => Ok(result),
        Err(e) if e.is_rate_limit() => {
            Err(ActivityError::Retryable {
                source: Box::new(e),
                explicit_delay: Some(Duration::from_secs(e.retry_after())),
            })
        }
        Err(e) if e.is_permanent() => {
            Err(ActivityError::NonRetryable(Box::new(e)))
        }
        Err(e) => {
            // Default: retryable
            Err(ActivityError::from(anyhow::anyhow!(e)))
        }
    }
}
```

### Workflow with Activity Error Handling

```rust
#[run]
pub async fn run(ctx: &mut WorkflowContext<Self>) -> WorkflowResult<OrderResult> {
    let payment_result = ctx.start_activity(
        MyActivities::process_payment,
        payment_req,
        ActivityOptions {
            start_to_close_timeout: Some(Duration::from_secs(30)),
            retry_policy: Some(RetryPolicy {
                maximum_attempts: 5,
                initial_interval: Duration::from_secs(1),
                backoff_coefficient: 2.0,
                maximum_interval: Some(Duration::from_secs(30)),
                non_retryable_error_types: vec!["InvalidInput".to_string()],
            }),
            ..Default::default()
        },
    ).await;

    match payment_result {
        Ok(result) => {
            ctx.state_mut(|s| s.status = "paid".to_string());
            Ok(OrderResult::Success(result))
        }
        Err(failure) => {
            ctx.state_mut(|s| s.status = "payment_failed".to_string());
            Err(anyhow::anyhow!("Payment failed: {}", failure))
        }
    }
}
```
