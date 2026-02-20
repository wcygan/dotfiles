# Cancellation

**Source**: https://docs.temporal.io/develop/go/cancellation

## Workflow Cancellation

When a client calls `CancelWorkflow`, the workflow's context is cancelled. Use a disconnected context for cleanup work.

### Handling cancellation in a workflow

```go
func MyWorkflow(ctx workflow.Context) error {
    // Disconnected context for cleanup — not cancelled when parent is cancelled
    cleanupCtx, _ := workflow.NewDisconnectedContext(ctx)

    defer func() {
        if ctx.Err() == workflow.ErrCanceled {
            // Run cleanup with disconnected context (not affected by cancellation)
            workflow.ExecuteActivity(cleanupCtx, CleanupActivity).Get(cleanupCtx, nil)
        }
    }()

    ao := workflow.ActivityOptions{
        StartToCloseTimeout: 10 * time.Minute,
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

    return workflow.ExecuteActivity(ctx, MainActivity).Get(ctx, nil)
}
```

### Cancel via client

```go
err = c.CancelWorkflow(context.Background(), workflowID, runID)
```

After calling `CancelWorkflow`:
1. Temporal server delivers a cancellation request to the next workflow task
2. The workflow's `ctx.Err()` returns `workflow.ErrCanceled`
3. Any `ExecuteActivity` blocked on `.Get()` returns a `CanceledError`
4. The workflow must handle the cancellation and return (typically `temporal.NewCanceledError()`)

### Returning cancellation error

```go
func MyWorkflow(ctx workflow.Context) error {
    err := workflow.ExecuteActivity(ctx, MyActivity).Get(ctx, nil)
    if err != nil {
        if temporal.IsCanceledError(err) {
            return temporal.NewCanceledError() // propagate cancellation
        }
        return err
    }
    return nil
}
```

## Activity Cancellation

Activities detect cancellation through heartbeats. An activity that doesn't heartbeat won't know it's been cancelled.

### Detecting cancellation via heartbeat

```go
func LongRunningActivity(ctx context.Context) error {
    for {
        doSomeWork()

        // RecordHeartbeat also checks cancellation
        activity.RecordHeartbeat(ctx)

        // Explicit check
        if ctx.Err() != nil {
            log.Println("Activity cancelled, stopping work")
            return temporal.NewCanceledError()
        }
    }
}
```

### WaitForCancellation option

By default, when the workflow cancels an activity, it returns immediately. Set `WaitForCancellation: true` to wait for the activity to finish:

```go
ao := workflow.ActivityOptions{
    StartToCloseTimeout: 10 * time.Minute,
    HeartbeatTimeout:    30 * time.Second,
    WaitForCancellation: true,  // wait for activity to complete/fail
}
ctx = workflow.WithActivityOptions(ctx, ao)
```

### Activity cancellation through workflow context

```go
func MyWorkflow(ctx workflow.Context) error {
    actCtx, cancelActivity := workflow.WithCancel(ctx)

    // Start activity in goroutine
    actFuture := workflow.ExecuteActivity(actCtx, LongActivity)

    // Cancel the activity after some condition
    selector := workflow.NewSelector(ctx)
    selector.AddFuture(actFuture, func(f workflow.Future) {})

    // Wait on signal or activity completion
    signalCh := workflow.GetSignalChannel(ctx, "cancel-activity")
    selector.AddReceive(signalCh, func(c workflow.ReceiveChannel, more bool) {
        cancelActivity()  // cancel the activity
    })

    selector.Select(ctx)
    return actFuture.Get(ctx, nil)
}
```

## Child Workflow Cancellation

```go
func ParentWorkflow(ctx workflow.Context) error {
    childCtx, cancelChild := workflow.WithCancel(ctx)

    childFuture := workflow.ExecuteChildWorkflow(childCtx, ChildWorkflow)

    // Cancel child after 5 seconds
    _ = workflow.Sleep(ctx, 5*time.Second)
    cancelChild()

    err := childFuture.Get(ctx, nil)
    if temporal.IsCanceledError(err) {
        log.Println("Child was cancelled successfully")
        return nil
    }
    return err
}
```

## Cancellation Patterns Summary

| Scenario | How to Detect | How to Respond |
|----------|---------------|----------------|
| Workflow cancelled by client | `ctx.Err() == workflow.ErrCanceled` | Cleanup with disconnected ctx, return `CanceledError` |
| Activity cancelled by workflow | `ctx.Err() != nil` in activity | Stop work, return `CanceledError` |
| Activity cancelled without heartbeat | Activity is force-cancelled after `HeartbeatTimeout` | N/A — can't detect |
| Child workflow cancelled | `temporal.IsCanceledError(err)` | Handle in parent workflow |
