# UI Metadata

**Source**: https://docs.temporal.io/develop/go/ui-metadata

UI Metadata lets you set human-readable summaries and descriptions for workflows, activities, and timers that appear in the Temporal Web UI and CLI.

## Workflow Summary and Details

### StaticSummary and StaticDetails (set at start)

Use `workflow.WithWorkflowMetadata` on the workflow context at startup:

```go
func OrderWorkflow(ctx workflow.Context, order Order) error {
    // Set static metadata visible in the Web UI
    if err := workflow.SetCurrentDetails(ctx, fmt.Sprintf(
        "Processing order %s for customer %s — $%.2f",
        order.ID, order.CustomerName, order.Total,
    )); err != nil {
        return err
    }

    // ... workflow logic ...
    return nil
}
```

### Dynamic updates with SetCurrentDetails

Update the workflow's description as it progresses:

```go
func LongRunningWorkflow(ctx workflow.Context, input Input) error {
    _ = workflow.SetCurrentDetails(ctx, "Starting — validating input")

    if err := workflow.ExecuteActivity(ctx, ValidateActivity, input).Get(ctx, nil); err != nil {
        return err
    }

    _ = workflow.SetCurrentDetails(ctx, "Validation complete — processing data")

    if err := workflow.ExecuteActivity(ctx, ProcessActivity, input).Get(ctx, nil); err != nil {
        return err
    }

    _ = workflow.SetCurrentDetails(ctx, "Processing complete — sending notifications")

    return workflow.ExecuteActivity(ctx, NotifyActivity, input).Get(ctx, nil)
}
```

### Reading current details

```go
details := workflow.GetCurrentDetails(ctx)
workflow.GetLogger(ctx).Info("Current details", "details", details)
```

## Setting Metadata at Workflow Start

Set `StaticSummary` and `StaticDetails` via `StartWorkflowOptions`:

```go
we, err := c.ExecuteWorkflow(ctx, client.StartWorkflowOptions{
    ID:        "order-workflow-123",
    TaskQueue: "orders",
    TypedSearchAttributes: temporal.NewSearchAttributes(...),
    WorkflowExecutionMetadata: &common.WorkflowExecutionMetadata{
        StaticSummary: "Order #123 — customer checkout flow",
        StaticDetails: "Customer: John Doe, Items: 3, Total: $150.00",
    },
}, OrderWorkflow, order)
```

## Activity Summary

Set a human-readable summary for activity appearances in the Web UI timeline:

```go
ao := workflow.ActivityOptions{
    StartToCloseTimeout: 10 * time.Second,
    Summary: "Charge payment card",  // appears in Web UI activity list
}
ctx = workflow.WithActivityOptions(ctx, ao)

if err := workflow.ExecuteActivity(ctx, ChargeCardActivity, payment).Get(ctx, nil); err != nil {
    return err
}
```

## Timer Summary

Add a description to timers so they're meaningful in the Web UI:

```go
timerCtx, cancel := workflow.WithCancel(ctx)
defer cancel()

timer := workflow.NewTimerWithOptions(timerCtx, 24*time.Hour, workflow.TimerOptions{
    Summary: "Waiting 24h for payment confirmation",
})

// Or with Sleep (no cancellation):
workflow.Sleep(ctx, 24*time.Hour)
// Note: Sleep doesn't support summary; use NewTimer for named timers
```

## Size Constraints

| Field | Max Size |
|-------|----------|
| `StaticSummary` | 400 bytes |
| `StaticDetails` | 20,000 bytes |
| `SetCurrentDetails` value | 20,000 bytes |
| Activity `Summary` | 400 bytes |
| Timer `Summary` | 400 bytes |

Values exceeding limits are truncated automatically.

## Web UI Visibility

| Metadata | Where Visible |
|----------|---------------|
| `StaticSummary` | Workflow list, workflow detail header |
| `StaticDetails` | Workflow detail page |
| `SetCurrentDetails` | Workflow detail page (updates live) |
| Activity `Summary` | Event history timeline |
| Timer `Summary` | Event history timeline |
