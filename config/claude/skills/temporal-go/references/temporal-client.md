# Temporal Client

**Source**: https://docs.temporal.io/develop/go/temporal-clients

## Client Creation

```go
import (
    "go.temporal.io/sdk/client"
)

c, err := client.Dial(client.Options{
    HostPort:  "localhost:7233",  // default
    Namespace: "default",        // default
})
if err != nil {
    log.Fatal(err)
}
defer c.Close()
```

### Configuration Methods

**1. Programmatic (recommended for production)**

```go
c, err := client.Dial(client.Options{
    HostPort:  "your-server:7233",
    Namespace: "your-namespace",
    ConnectionOptions: client.ConnectionOptions{
        TLS: &tls.Config{...},
    },
})
```

**2. Environment variables**

```bash
TEMPORAL_ADDRESS=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TLS_CERT=/path/to/cert.pem
TEMPORAL_TLS_KEY=/path/to/key.pem
```

**3. TOML config file** (`~/.config/temporalio/temporal.toml`)

```toml
[connection.default]
address = "localhost:7233"
namespace = "default"
```

## Temporal Cloud Connection

### mTLS Authentication

```go
cert, err := tls.LoadX509KeyPair("client.pem", "client.key")
if err != nil {
    log.Fatal(err)
}

c, err := client.Dial(client.Options{
    HostPort:  "your-namespace.tmprl.cloud:7233",
    Namespace: "your-namespace.your-account",
    ConnectionOptions: client.ConnectionOptions{
        TLS: &tls.Config{
            Certificates: []tls.Certificate{cert},
        },
    },
})
```

### API Key Authentication

```go
c, err := client.Dial(client.Options{
    HostPort:  "us-east-1.aws.api.temporal.io:7233",
    Namespace: "your-namespace.your-account",
    Credentials: client.NewAPIKeyStaticCredentials("your-api-key"),
    ConnectionOptions: client.ConnectionOptions{
        TLS: &tls.Config{},  // required for Cloud even without mTLS
    },
})
```

### Dynamic credentials (key rotation)

```go
c, err := client.Dial(client.Options{
    HostPort:  "us-east-1.aws.api.temporal.io:7233",
    Namespace: "your-namespace.your-account",
    Credentials: client.NewAPIKeyDynamicCredentials(func(ctx context.Context) (string, error) {
        return loadKeyFromVault(ctx)
    }),
    ConnectionOptions: client.ConnectionOptions{
        TLS: &tls.Config{},
    },
})
```

## Starting Workflows

```go
we, err := c.ExecuteWorkflow(
    context.Background(),
    client.StartWorkflowOptions{
        ID:        "transfer-workflow-001",
        TaskQueue: "money-transfer",
    },
    TransferMoneyWorkflow,
    TransferInput{FromAccount: "A", ToAccount: "B", Amount: 100.0},
)
if err != nil {
    log.Fatal(err)
}
log.Printf("Started: WorkflowID=%s RunID=%s", we.GetID(), we.GetRunID())
```

### StartWorkflowOptions

| Field | Default | Description |
|-------|---------|-------------|
| `ID` | auto-generated | Unique workflow ID (idempotency key) |
| `TaskQueue` | Required | Which worker pool handles this |
| `WorkflowExecutionTimeout` | Unlimited | Max time for entire workflow (including retries) |
| `WorkflowRunTimeout` | Unlimited | Max time for a single run |
| `WorkflowTaskTimeout` | 10s | Max time for single workflow task |
| `WorkflowIDReusePolicy` | `AllowDuplicate` | What to do if ID already exists |
| `WorkflowIDConflictPolicy` | `Fail` | What to do if workflow is running |
| `RetryPolicy` | None | Retry the workflow on failure |
| `CronSchedule` | None | Cron expression for periodic execution |
| `Memo` | None | Unindexed key-value metadata |
| `SearchAttributes` | None | Indexed, searchable attributes |
| `StartDelay` | 0 | Delay before first workflow task |

### WorkflowIDReusePolicy Values

| Policy | Behavior |
|--------|----------|
| `AllowDuplicate` | Always allow (creates new run) |
| `AllowDuplicateFailedOnly` | Allow only if last run failed/cancelled |
| `RejectDuplicate` | Fail if any completed run exists |
| `TerminateIfRunning` | Terminate running workflow and start new |

## Getting Workflow Results

### Same process (immediate)

```go
we, _ := c.ExecuteWorkflow(ctx, opts, MyWorkflow, input)

var result MyResult
if err := we.Get(ctx, &result); err != nil {
    log.Fatal("Workflow failed:", err)
}
fmt.Println("Result:", result)
```

### Different process (by ID)

```go
we := c.GetWorkflow(ctx, workflowID, runID)

var result MyResult
if err := we.Get(ctx, &result); err != nil {
    log.Fatal(err)
}
```

### Non-blocking check

```go
var result MyResult
err := we.GetWithOptions(ctx, &result, client.WorkflowRunGetOptions{
    DisableFollowingRuns: true,
})
```

## Signals, Queries, and Updates

```go
// Send a signal
err = c.SignalWorkflow(ctx, workflowID, runID, "my-signal", signalPayload)

// Query workflow state
val, err := c.QueryWorkflow(ctx, workflowID, runID, "get-state")
var state string
val.Get(&state)

// Send an update (validated, synchronous)
handle, err := c.UpdateWorkflow(ctx, client.UpdateWorkflowOptions{
    WorkflowID: workflowID,
    UpdateName: "add-item",
    Args:       []interface{}{item},
    WaitForStage: client.WorkflowUpdateStageCompleted,
})
var updateResult string
handle.Get(ctx, &updateResult)
```

## Search Attributes

```go
// Built-in typed search attributes
sa := temporal.NewSearchAttributes(
    temporal.NewSearchAttributeKeyString("CustomerId").ValueSet("customer-123"),
    temporal.NewSearchAttributeKeyInt64("OrderAmount").ValueSet(int64(500)),
)

we, err := c.ExecuteWorkflow(ctx, client.StartWorkflowOptions{
    ID:               "order-workflow",
    TaskQueue:        "orders",
    TypedSearchAttributes: sa,
}, OrderWorkflow, input)
```

## Cron Workflows

```go
we, err := c.ExecuteWorkflow(ctx, client.StartWorkflowOptions{
    ID:           "daily-report",
    TaskQueue:    "reports",
    CronSchedule: "0 8 * * *",  // 8am UTC daily
}, DailyReportWorkflow)
```

Note: Use Temporal Schedules API for more control over scheduled workflows.

## Cancellation and Termination

```go
// Graceful cancellation (workflow handles it)
err = c.CancelWorkflow(ctx, workflowID, runID)

// Force terminate (no cleanup)
err = c.TerminateWorkflow(ctx, workflowID, runID, "manual termination", details...)
```
