# Core Application

**Source**: https://docs.temporal.io/develop/go/core-application

## SDK Installation

```bash
go get go.temporal.io/sdk
```

Start a local dev server (requires Temporal CLI):

```bash
temporal server start-dev
# Listens on localhost:7233, Web UI at localhost:8233
```

## Workflow Definition

A workflow is a regular Go function with a `workflow.Context` as its first parameter. It **must** be deterministic — all non-deterministic operations (I/O, time, randomness) must be delegated to activities.

```go
import "go.temporal.io/sdk/workflow"

func TransferMoneyWorkflow(ctx workflow.Context, input TransferInput) error {
    ao := workflow.ActivityOptions{
        StartToCloseTimeout: 10 * time.Second,
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

    // Execute activities — non-deterministic work happens here
    if err := workflow.ExecuteActivity(ctx, WithdrawActivity, input.Amount).Get(ctx, nil); err != nil {
        return err
    }
    return workflow.ExecuteActivity(ctx, DepositActivity, input.Amount).Get(ctx, nil)
}
```

### Workflow Constraints (Determinism Rules)

| Allowed | Forbidden |
|---------|-----------|
| `workflow.Now(ctx)` | `time.Now()` |
| `workflow.Sleep(ctx, d)` | `time.Sleep(d)` |
| `workflow.NewChannel(ctx)` | `make(chan T)` (direct) |
| `workflow.Go(ctx, fn)` | `go fn()` (direct goroutine) |
| `workflow.GetLogger(ctx)` | `log.Println()`, `fmt.Println()` |
| Reading workflow input args | Network/file I/O |
| `workflow.SideEffect` | `rand.Int()`, `uuid.New()` |

### Workflow-Only APIs

| API | Notes |
|-----|-------|
| `workflow.Now(ctx)` | Returns deterministic current time |
| `workflow.Sleep(ctx, d)` | Durable sleep; survives worker restarts |
| `workflow.Go(ctx, fn)` | Coroutine-style goroutine |
| `workflow.NewChannel(ctx)` | Typed channel |
| `workflow.NewBufferedChannel(ctx, n)` | Buffered channel |
| `workflow.NewSelector(ctx)` | Like `reflect.Select` for workflow Futures |
| `workflow.NewWaitGroup(ctx)` | Like `sync.WaitGroup` |
| `workflow.GetInfo(ctx)` | Returns `WorkflowInfo` (ID, run ID, task queue, etc.) |
| `workflow.GetLogger(ctx)` | Replay-safe logger |
| `workflow.UpsertMemo(ctx, memo)` | Update workflow memo |
| `workflow.UpsertTypedSearchAttributes(ctx, ...)` | Update search attributes |

### Signals

```go
func MyWorkflow(ctx workflow.Context) error {
    ch := workflow.GetSignalChannel(ctx, "my-signal")

    var payload string
    ch.Receive(ctx, &payload)  // blocks until signal arrives
    // process payload...
    return nil
}

// Send from client:
c.SignalWorkflow(ctx, workflowID, runID, "my-signal", "hello")
```

### Queries

```go
func MyWorkflow(ctx workflow.Context) error {
    state := "starting"
    workflow.SetQueryHandler(ctx, "get-state", func() (string, error) {
        return state, nil
    })
    // ... update state ...
    return nil
}

// Query from client:
val, err := c.QueryWorkflow(ctx, workflowID, runID, "get-state")
```

### Updates (validated mutations)

```go
workflow.SetUpdateHandlerWithOptions(ctx, "add-item", func(ctx workflow.Context, item string) error {
    // mutate state
    return nil
}, workflow.UpdateHandlerOptions{
    Validator: func(ctx workflow.Context, item string) error {
        if item == "" {
            return errors.New("item cannot be empty")
        }
        return nil
    },
})
```

## Activity Definition

Activities perform side-effecting work (I/O, external calls). They can be plain functions or methods on a struct (for shared dependencies).

### Function-based

```go
import "go.temporal.io/sdk/activity"

func EmailActivity(ctx context.Context, email string) error {
    // real I/O here — no determinism constraint
    return sendEmail(email)
}
```

### Struct-based (recommended for shared resources)

```go
type Activities struct {
    db     *sql.DB
    client *http.Client
}

func (a *Activities) CreateOrderActivity(ctx context.Context, order Order) (string, error) {
    return a.db.InsertOrder(ctx, order)
}

func (a *Activities) NotifyActivity(ctx context.Context, msg string) error {
    return a.client.Post("/notify", msg)
}
```

### ActivityOptions

Set on the workflow context before calling `ExecuteActivity`:

```go
ao := workflow.ActivityOptions{
    TaskQueue:              "my-task-queue",    // override default
    ScheduleToCloseTimeout: 5 * time.Minute,   // total time allowed
    StartToCloseTimeout:    10 * time.Second,  // per-attempt time limit
    ScheduleToStartTimeout: 30 * time.Second,  // time to pick up
    HeartbeatTimeout:       5 * time.Second,   // heartbeat interval check
    RetryPolicy: &temporal.RetryPolicy{
        InitialInterval:    time.Second,
        BackoffCoefficient: 2.0,
        MaximumInterval:    100 * time.Second,
        MaximumAttempts:    5,
    },
    WaitForCancellation: false, // return immediately on cancel
}
ctx = workflow.WithActivityOptions(ctx, ao)
```

| Field | Default | Description |
|-------|---------|-------------|
| `ScheduleToCloseTimeout` | Unlimited | Max time from schedule to completion |
| `StartToCloseTimeout` | Required | Max time for a single attempt |
| `ScheduleToStartTimeout` | Unlimited | Max time waiting in queue |
| `HeartbeatTimeout` | None | Max time between heartbeats |
| `RetryPolicy.MaximumAttempts` | Unlimited | 0 means unlimited retries |
| `RetryPolicy.NonRetryableErrorTypes` | `[]` | Error types that skip retry |

## Worker Setup

A worker hosts both workflow and activity executions. It polls a task queue.

```go
import (
    "go.temporal.io/sdk/client"
    "go.temporal.io/sdk/worker"
)

func main() {
    c, err := client.Dial(client.Options{})
    if err != nil {
        log.Fatal(err)
    }
    defer c.Close()

    w := worker.New(c, "my-task-queue", worker.Options{})

    // Register workflows and activities
    w.RegisterWorkflow(TransferMoneyWorkflow)
    w.RegisterActivity(WithdrawActivity)
    w.RegisterActivity(DepositActivity)

    // For struct-based activities, register the struct instance
    acts := &Activities{db: db, client: httpClient}
    w.RegisterActivity(acts)

    // Run blocks until interrupted
    if err := w.Run(worker.InterruptCh()); err != nil {
        log.Fatal(err)
    }
}
```

### Worker Options

| Option | Default | Description |
|--------|---------|-------------|
| `MaxConcurrentActivityExecutionSize` | 1000 | Max parallel activities |
| `MaxConcurrentWorkflowTaskExecutionSize` | 1000 | Max parallel workflow tasks |
| `MaxConcurrentLocalActivityExecutionSize` | 1000 | Max parallel local activities |
| `WorkflowPanicPolicy` | `BlockWorkflow` | On panic: block or fail |
| `EnableLoggingInReplay` | false | Show logs during replay |

## Dynamic Workflows and Activities

Register using string names instead of function references:

```go
w.RegisterWorkflowWithOptions(MyWorkflow, workflow.RegisterOptions{
    Name: "custom-workflow-name",
})

w.RegisterActivityWithOptions(MyActivity, activity.RegisterOptions{
    Name: "custom-activity-name",
})
```

Execute by name from a workflow:

```go
workflow.ExecuteActivity(ctx, "custom-activity-name", args...)
workflow.ExecuteChildWorkflow(ctx, "custom-workflow-name", args...)
```

## Key Design Patterns

### Use parameter objects for future-proofing

```go
// Good — can add fields without breaking existing workflows
type TransferInput struct {
    FromAccount string
    ToAccount   string
    Amount      float64
}

// Avoid — positional args break on workflow version changes
func BadWorkflow(ctx workflow.Context, from, to string, amount float64) error
```

### Payload size limits

- Default max payload per message: 4 MB (configurable)
- Large data: store in blob storage, pass reference IDs through Temporal

### Local activities

For short-lived (<= few seconds), non-retriable work to avoid round-trips to the server:

```go
ctx = workflow.WithLocalActivityOptions(ctx, workflow.LocalActivityOptions{
    StartToCloseTimeout: 5 * time.Second,
})
workflow.ExecuteLocalActivity(ctx, MyActivity, args...)
```
