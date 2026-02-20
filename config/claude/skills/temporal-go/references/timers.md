# Timers

**Source**: https://docs.temporal.io/develop/go/timers

## Overview

Temporal timers are durable — they survive worker and server restarts. The workflow will resume exactly when the timer fires, regardless of downtime.

**Never use `time.Sleep` in a workflow** — it is non-deterministic and won't survive restarts. Always use `workflow.Sleep` or `workflow.NewTimer`.

## workflow.Sleep

Simple, non-cancellable pause:

```go
func ReminderWorkflow(ctx workflow.Context, userID string) error {
    // Wait 24 hours durably
    if err := workflow.Sleep(ctx, 24*time.Hour); err != nil {
        // err is non-nil if the workflow was cancelled during sleep
        return temporal.NewCanceledError()
    }

    return workflow.ExecuteActivity(ctx, SendReminderActivity, userID).Get(ctx, nil)
}
```

## workflow.NewTimer

Cancellable timer returning a `workflow.Future`:

```go
func TimeoutPatternWorkflow(ctx workflow.Context) error {
    timerCtx, cancelTimer := workflow.WithCancel(ctx)
    defer cancelTimer()

    // Create a 10-minute timer
    timer := workflow.NewTimer(timerCtx, 10*time.Minute)

    // Create the main work future
    actFuture := workflow.ExecuteActivity(ctx, DoWorkActivity)

    // Race: activity vs timer
    selector := workflow.NewSelector(ctx)

    selector.AddFuture(actFuture, func(f workflow.Future) {
        cancelTimer() // cancel the timer if activity finishes first
    })

    selector.AddFuture(timer, func(f workflow.Future) {
        if f.Get(ctx, nil) == nil {
            // Timer fired — activity timed out from our perspective
            workflow.GetLogger(ctx).Info("Activity timeout exceeded")
        }
    })

    selector.Select(ctx)
    return actFuture.Get(ctx, nil)
}
```

## NewTimerWithOptions (with summary)

```go
timer := workflow.NewTimerWithOptions(ctx, 24*time.Hour, workflow.TimerOptions{
    Summary: "Waiting for payment window to close",
})
timer.Get(ctx, nil) // wait for timer
```

## Durability Guarantees

- Timers are persisted to the Temporal Server — process crashes don't affect them
- Timer resolution is approximately 1 second
- Very short timers (< 1 second) still work but aren't more precise than 1 second
- Timers with zero or negative duration fire immediately

## Common Patterns

### Scheduled delay before action

```go
func ScheduledActionWorkflow(ctx workflow.Context, delay time.Duration) error {
    workflow.Sleep(ctx, delay)
    return workflow.ExecuteActivity(ctx, TakeActionActivity).Get(ctx, nil)
}
```

### Retry with delay

```go
for attempt := 0; attempt < 3; attempt++ {
    err := workflow.ExecuteActivity(ctx, MyActivity).Get(ctx, nil)
    if err == nil {
        return nil
    }
    if attempt < 2 {
        workflow.Sleep(ctx, time.Duration(attempt+1)*time.Minute)
    }
}
return errors.New("all attempts failed")
```

### Deadline enforcement

```go
func WithDeadline(ctx workflow.Context, deadline time.Time) (workflow.Context, func()) {
    remaining := workflow.Now(ctx).Sub(deadline)
    if remaining <= 0 {
        // Already past deadline
        cancelCtx, cancel := workflow.WithCancel(ctx)
        cancel()
        return cancelCtx, cancel
    }
    timerCtx, cancelTimer := workflow.WithCancel(ctx)
    timer := workflow.NewTimer(timerCtx, remaining)
    go func() {
        timer.Get(timerCtx, nil)
        cancelTimer()
    }()
    return timerCtx, cancelTimer
}
```

## What NOT to Do

```go
// WRONG — time.Sleep is not durable, breaks determinism
func BadWorkflow(ctx workflow.Context) error {
    time.Sleep(24 * time.Hour) // DON'T DO THIS
    return nil
}

// WRONG — time.Now() is non-deterministic in workflows
func AlsoBad(ctx workflow.Context) error {
    now := time.Now() // DON'T DO THIS
    // use workflow.Now(ctx) instead
    return nil
}
```
