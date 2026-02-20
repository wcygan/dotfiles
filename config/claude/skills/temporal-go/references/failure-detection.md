# Failure Detection

**Source**: https://docs.temporal.io/develop/go/failure-detection

## Workflow Timeouts

Set on `StartWorkflowOptions`. Timeouts apply to the entire workflow lifecycle.

| Timeout | Scope | Typical Use |
|---------|-------|-------------|
| `WorkflowExecutionTimeout` | Entire workflow (all runs) | Hard deadline across all retries |
| `WorkflowRunTimeout` | Single workflow run | Per-run deadline |
| `WorkflowTaskTimeout` | Single workflow task (code execution) | Detect infinite loops (max 60s) |

```go
we, err := c.ExecuteWorkflow(ctx, client.StartWorkflowOptions{
    ID:                       "order-workflow",
    TaskQueue:                "orders",
    WorkflowExecutionTimeout: 30 * time.Minute,
    WorkflowRunTimeout:       10 * time.Minute,
    WorkflowTaskTimeout:      10 * time.Second,
}, OrderWorkflow, input)
```

## Workflow Retry Policy

Workflows can be retried on failure (not on cancellation or termination):

```go
we, err := c.ExecuteWorkflow(ctx, client.StartWorkflowOptions{
    ID:        "order-workflow",
    TaskQueue: "orders",
    RetryPolicy: &temporal.RetryPolicy{
        InitialInterval:        time.Second,
        BackoffCoefficient:     2.0,
        MaximumInterval:        100 * time.Second,
        MaximumAttempts:        5,
        NonRetryableErrorTypes: []string{"InvalidInputError"},
    },
}, OrderWorkflow, input)
```

## Activity Timeouts

Set per-activity via `ActivityOptions`. **`StartToCloseTimeout` is required** (or `ScheduleToCloseTimeout`).

| Timeout | Scope | Notes |
|---------|-------|-------|
| `ScheduleToCloseTimeout` | Schedule → final completion | Overall deadline per attempt + retries |
| `StartToCloseTimeout` | Start → completion of one attempt | **Required**; max execution time per try |
| `ScheduleToStartTimeout` | Schedule → worker picks up | Detect queue backup; rarely needed |
| `HeartbeatTimeout` | Max time between heartbeats | Must be set to detect activity failure |

```go
ao := workflow.ActivityOptions{
    StartToCloseTimeout:    10 * time.Second,   // required
    ScheduleToCloseTimeout: 5 * time.Minute,    // optional overall cap
    HeartbeatTimeout:       30 * time.Second,   // detect unresponsive activities
}
ctx = workflow.WithActivityOptions(ctx, ao)
```

## Activity Retry Policy

Default retry behavior: unlimited retries with exponential backoff.

```go
ao := workflow.ActivityOptions{
    StartToCloseTimeout: 10 * time.Second,
    RetryPolicy: &temporal.RetryPolicy{
        InitialInterval:    time.Second,       // first retry after 1s
        BackoffCoefficient: 2.0,               // doubles each retry
        MaximumInterval:    100 * time.Second, // cap backoff at 100s
        MaximumAttempts:    3,                 // 0 = unlimited
        NonRetryableErrorTypes: []string{
            "InvalidInputError",
            "AuthorizationError",
        },
    },
}
```

### Default retry values

| Parameter | Default |
|-----------|---------|
| `InitialInterval` | 1 second |
| `BackoffCoefficient` | 2.0 |
| `MaximumInterval` | 100 × InitialInterval |
| `MaximumAttempts` | 0 (unlimited) |
| `NonRetryableErrorTypes` | `[]` (all retryable) |

### Non-retryable errors

Mark an error as non-retryable in the activity:

```go
func MyActivity(ctx context.Context, input string) error {
    if input == "" {
        return temporal.NewApplicationError(
            "input is required",
            "InvalidInputError",  // type name for NonRetryableErrorTypes
        )
    }
    return nil
}
```

Or use `ApplicationErrorOptions`:

```go
return temporal.NewApplicationErrorWithOptions(
    "input required",
    temporal.ApplicationErrorOptions{
        Type:        "InvalidInputError",
        NonRetryable: true,
    },
)
```

## Activity Heartbeats

Heartbeats allow Temporal to detect unresponsive activities and recover state after restarts.

### Basic heartbeat

```go
func LongRunningActivity(ctx context.Context, jobID string) error {
    for i := 0; i < 1000; i++ {
        // Do a unit of work
        processChunk(i)

        // Heartbeat with progress
        activity.RecordHeartbeat(ctx, i)

        // Check if cancelled
        if ctx.Err() != nil {
            return temporal.NewCanceledError()
        }
    }
    return nil
}
```

**Important**: `RecordHeartbeat` checks `ctx` cancellation — if the activity is cancelled, the next heartbeat will return a cancelled context and you should stop work.

### Recovering progress after retry

```go
func LongRunningActivity(ctx context.Context) error {
    startIndex := 0

    // Recover from previous failed attempt
    if activity.HasHeartbeatDetails(ctx) {
        var lastIndex int
        if err := activity.GetHeartbeatDetails(ctx, &lastIndex); err == nil {
            startIndex = lastIndex + 1
            log.Printf("Resuming from index %d", startIndex)
        }
    }

    for i := startIndex; i < 1000; i++ {
        processItem(i)
        activity.RecordHeartbeat(ctx, i) // save progress
    }
    return nil
}
```

### Heartbeat interval recommendation

Set `HeartbeatTimeout` to 2-3× the expected interval between heartbeat calls:

```go
ao := workflow.ActivityOptions{
    StartToCloseTimeout: 30 * time.Minute,
    HeartbeatTimeout:    30 * time.Second, // if you heartbeat every ~10s
}
```

## Custom Retry Delay

Use `ApplicationErrorOptions.NextRetryDelay` to override backoff for a specific error:

```go
func APIActivity(ctx context.Context) error {
    resp, err := callAPI()
    if err != nil {
        if isRateLimited(resp) {
            retryAfter := parseRetryAfter(resp)
            return temporal.NewApplicationErrorWithOptions(
                "rate limited",
                temporal.ApplicationErrorOptions{
                    Type:           "RateLimited",
                    NextRetryDelay: retryAfter,
                },
            )
        }
        return err
    }
    return nil
}
```

## Detecting Workflow Timeout in the Workflow

```go
func MyWorkflow(ctx workflow.Context) error {
    // DeadlineExceeded means the workflow task timed out
    childCtx, cancel := workflow.WithCancel(ctx)
    defer cancel()

    err := workflow.ExecuteActivity(childCtx, MyActivity).Get(childCtx, nil)
    if temporal.IsTimeoutError(err) {
        te := err.(*temporal.TimeoutError)
        log.Printf("Timed out: type=%v", te.TimeoutType())
    }
    return err
}
```

## Error Types

| Error Type | Description |
|------------|-------------|
| `temporal.ApplicationError` | Business logic failure, optionally retryable |
| `temporal.TimeoutError` | Activity or workflow timed out |
| `temporal.CanceledError` | Workflow/activity was cancelled |
| `temporal.PanicError` | Workflow panicked (non-determinism or bug) |
| `temporal.TerminatedError` | Workflow was force-terminated |
