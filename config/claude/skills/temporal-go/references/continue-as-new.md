# Continue-As-New

**Source**: https://docs.temporal.io/develop/go/continue-as-new

## Overview

Temporal workflows store all events in an event history. For long-running workflows with unbounded loops, the history can grow too large (default limit: 50,000 events, ~50 MB). `ContinueAsNew` starts a fresh workflow run with a clean history, carrying state forward via new input arguments.

## Basic Usage

```go
func SubscriptionWorkflow(ctx workflow.Context, customerID string, billingCycle int) error {
    // ... do work for this billing cycle ...
    if err := workflow.ExecuteActivity(ctx, BillCustomerActivity, customerID, billingCycle).Get(ctx, nil); err != nil {
        return err
    }

    // Wait until next billing date
    workflow.Sleep(ctx, 30*24*time.Hour)

    // Continue as new — starts fresh run with updated args
    return workflow.NewContinueAsNewError(ctx, SubscriptionWorkflow, customerID, billingCycle+1)
}
```

The returned error from `workflow.NewContinueAsNewError` causes Temporal to:
1. Complete the current run
2. Start a new run of the same workflow with the provided arguments
3. Preserve the same workflow ID

## Checking When to Continue-As-New

Use `workflow.GetInfo(ctx).GetContinueAsNewSuggested()` to check if Temporal recommends continuing:

```go
func EventProcessingWorkflow(ctx workflow.Context, state ProcessingState) error {
    for {
        // Process one event
        var event Event
        if err := workflow.ExecuteActivity(ctx, FetchNextEventActivity).Get(ctx, &event); err != nil {
            return err
        }

        state = processEvent(state, event)

        // Check if we should continue-as-new
        if workflow.GetInfo(ctx).GetContinueAsNewSuggested() {
            return workflow.NewContinueAsNewError(ctx, EventProcessingWorkflow, state)
        }
    }
}
```

## State Carryover Pattern

Design your workflow input to be the complete state needed for a new run:

```go
type WorkflowState struct {
    ProcessedCount int
    LastOffset     string
    Checksum       string
    StartedAt      time.Time
}

func DataSyncWorkflow(ctx workflow.Context, state WorkflowState) error {
    const maxIterations = 100

    for i := 0; i < maxIterations; i++ {
        var result SyncResult
        if err := workflow.ExecuteActivity(ctx, SyncBatchActivity, state.LastOffset).Get(ctx, &result); err != nil {
            return err
        }

        state.ProcessedCount += result.Count
        state.LastOffset = result.NextOffset

        if result.Done {
            return nil // natural completion
        }

        if workflow.GetInfo(ctx).GetContinueAsNewSuggested() {
            return workflow.NewContinueAsNewError(ctx, DataSyncWorkflow, state)
        }
    }

    // Safety: always continue after maxIterations regardless
    return workflow.NewContinueAsNewError(ctx, DataSyncWorkflow, state)
}
```

## Signal and Update Handler Constraints

Signal and update handlers **must drain** before continue-as-new or the pending messages are lost. Use `workflow.AllHandlersFinished`:

```go
func MyWorkflow(ctx workflow.Context) error {
    updateCh := workflow.GetSignalChannel(ctx, "my-update")

    var pendingUpdates []string
    workflow.Go(ctx, func(ctx workflow.Context) {
        for {
            var update string
            updateCh.Receive(ctx, &update)
            pendingUpdates = append(pendingUpdates, update)
        }
    })

    // Process work...
    workflow.Sleep(ctx, time.Hour)

    // Wait for all signal/update handlers to complete before CAN
    _ = workflow.Await(ctx, func() bool {
        return workflow.AllHandlersFinished(ctx)
    })

    return workflow.NewContinueAsNewError(ctx, MyWorkflow)
}
```

## Testing Continue-As-New

Test CAN workflows by limiting history length in tests:

```go
func (s *UnitTestSuite) Test_ContinueAsNew() {
    // Configure the env to suggest CAN after 3 events
    s.env.SetContinueAsNewSuggested(true)

    // Capture which workflow is continued into
    var continuedWith interface{}
    s.env.SetOnContinueAsNewListener(func(workflowFn interface{}, args ...interface{}) {
        continuedWith = workflowFn
    })

    s.env.ExecuteWorkflow(MyWorkflow, initialState)

    s.True(s.env.IsWorkflowCompleted())
    // Workflow should have continued-as-new
    s.NotNil(continuedWith)
}
```

## ContinueAsNew vs Other Patterns

| Pattern | Use When |
|---------|----------|
| `ContinueAsNew` | Unbounded loops, long-lived workflows (months/years) |
| Child Workflow | Bounded sub-tasks, fan-out/fan-in |
| Activity | Side effects, external I/O, non-deterministic work |
| `workflow.Sleep` | Fixed-duration waits within a bounded run |

## History Size Limits

| Limit | Default | Configurable |
|-------|---------|-------------|
| Max history events | 50,000 | Yes (server config) |
| Max history size | ~50 MB | Yes (server config) |
| `GetContinueAsNewSuggested()` triggers at | ~10,000 events | Yes |

Start considering CAN well before hitting the hard limit — `GetContinueAsNewSuggested()` returns `true` at ~10,000 events by default.
