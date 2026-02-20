# Async Activity Completion

**Source**: https://docs.temporal.io/develop/go/async-activity-completion

## Overview

Async activity completion allows an activity to return `activity.ErrResultPending` and be completed later by an external process using a task token or workflow+activity ID. This is used for human-approval workflows, external system callbacks, or any long-running integration.

## Three-Step Pattern

### Step 1: Get the task token and return ErrResultPending

```go
func HumanApprovalActivity(ctx context.Context, request ApprovalRequest) error {
    // Get task token — used to complete the activity later
    info := activity.GetInfo(ctx)
    taskToken := info.TaskToken

    // Store the task token externally (database, message queue, etc.)
    err := db.SavePendingApproval(request.ID, taskToken)
    if err != nil {
        return err // return real error — won't be treated as pending
    }

    // Send approval request to human reviewer
    err = notifyReviewer(request, taskToken)
    if err != nil {
        return err
    }

    // Signal Temporal that this activity will be completed externally
    return activity.ErrResultPending
}
```

### Step 2: External system completes the activity

```go
// Called by webhook, UI callback, or external service
func HandleApprovalDecision(c client.Client, taskToken []byte, approved bool) error {
    ctx := context.Background()

    if approved {
        result := ApprovalResult{Approved: true}
        return c.CompleteActivity(ctx, taskToken, result, nil)
    }

    return c.CompleteActivity(ctx, taskToken, nil,
        temporal.NewApplicationError("approval denied", "ApprovalDenied"))
}
```

### Step 3: Workflow receives the result normally

```go
func OrderWorkflow(ctx workflow.Context, order Order) error {
    ao := workflow.ActivityOptions{
        StartToCloseTimeout: 24 * time.Hour, // long timeout for human approval
        HeartbeatTimeout:    0,              // no heartbeat required for async
    }
    ctx = workflow.WithActivityOptions(ctx, ao)

    var approvalResult ApprovalResult
    err := workflow.ExecuteActivity(ctx, HumanApprovalActivity, order).Get(ctx, &approvalResult)
    if err != nil {
        return fmt.Errorf("approval failed: %w", err)
    }

    // Continue processing
    return workflow.ExecuteActivity(ctx, FulfillOrderActivity, order).Get(ctx, nil)
}
```

## Identifying Activities

### By task token (preferred)

```go
// Most reliable — uniquely identifies the exact activity attempt
c.CompleteActivity(ctx, taskToken, result, nil)
c.FailActivity(ctx, taskToken, err)
```

### By workflow ID + run ID + activity ID

```go
c.CompleteActivityByID(ctx,
    "your-namespace",
    workflowID,
    runID,
    activityID,   // from activity.GetInfo(ctx).ActivityID
    result,
    nil,
)
```

## Heartbeating Async Activities

Even async activities can send heartbeats to prevent timeout:

```go
func AsyncActivity(ctx context.Context) error {
    info := activity.GetInfo(ctx)
    taskToken := info.TaskToken

    // Store task token
    storeToken(taskToken)

    // Return pending
    return activity.ErrResultPending
}

// External process sends periodic heartbeats using the client
func HeartbeatAsyncActivity(c client.Client, taskToken []byte) error {
    return c.RecordActivityHeartbeat(context.Background(), taskToken, "still working")
}
```

## Failing an Async Activity

```go
// Complete with an error
c.CompleteActivity(ctx, taskToken, nil,
    temporal.NewApplicationError("processing failed", "ProcessingError"))

// Or use typed failure
c.CompleteActivity(ctx, taskToken, nil,
    temporal.NewApplicationErrorWithOptions("processing failed",
        temporal.ApplicationErrorOptions{
            Type:         "ProcessingError",
            NonRetryable: true,
        },
    ),
)
```

## Use Cases

| Use Case | Description |
|----------|-------------|
| Human-in-the-loop | Send task to UI; complete when human approves/rejects |
| External system callback | Trigger webhook; complete when system responds |
| Long-running integration | Hand off to external system; complete via callback |
| Message queue processing | Publish message; complete when consumer acknowledges |

## Important Notes

- The task token is opaque bytes — serialize with base64 for storage/transport
- Activity timeout still applies — set `StartToCloseTimeout` long enough
- The workflow has no idea the activity is async — it just waits for completion
- If the activity is not completed before timeout, it will be retried (new task token issued)
