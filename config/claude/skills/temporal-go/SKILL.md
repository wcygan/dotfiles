---
name: temporal-go
description: Temporal Go SDK expert for durable workflow orchestration. Auto-loads when working with Temporal workflows, activities, workers, workflow.Context, workflow.ExecuteActivity, temporal client, task queues, activity heartbeats, retry policies, workflow signals, queries, continue-as-new, workflow testing, TestWorkflowEnvironment, activity mocking, cancellation handling, workflow timers, or Temporal Cloud mTLS/API key configuration.
---

# Temporal Go SDK

Temporal is a durable execution platform that makes application code fault-tolerant and scalable. Workflows are ordinary Go functions that survive process restarts; activities are the side-effecting work units.

## Core API Quick Reference

### Workflow APIs (`go.temporal.io/sdk/workflow`)

| API | Purpose |
|-----|---------|
| `workflow.ExecuteActivity(ctx, fn, args...)` | Schedule an activity execution |
| `workflow.ExecuteChildWorkflow(ctx, fn, args...)` | Start a child workflow |
| `workflow.Sleep(ctx, duration)` | Durable timer pause |
| `workflow.NewTimer(ctx, duration)` | Cancellable timer Future |
| `workflow.Go(ctx, fn)` | Spawn a goroutine in workflow context |
| `workflow.NewChannel(ctx)` | Create a workflow-safe channel |
| `workflow.NewSelector(ctx)` | Create a selector for racing futures |
| `workflow.GetInfo(ctx)` | Get current workflow metadata |
| `workflow.GetLogger(ctx)` | Get replay-safe logger |
| `workflow.Now(ctx)` | Get deterministic current time |
| `workflow.NewContinueAsNewError(ctx, fn, args...)` | Continue-as-new |
| `workflow.SetQueryHandler(ctx, name, fn)` | Register query handler |
| `workflow.SetUpdateHandler(ctx, name, fn, opts)` | Register update handler |

### Activity APIs (`go.temporal.io/sdk/activity`)

| API | Purpose |
|-----|---------|
| `activity.GetInfo(ctx)` | Get activity metadata (task token, etc.) |
| `activity.RecordHeartbeat(ctx, details...)` | Send heartbeat + check cancellation |
| `activity.HasHeartbeatDetails(ctx)` | Check if previous attempt left details |
| `activity.GetHeartbeatDetails(ctx, &out)` | Recover heartbeat details after retry |
| `activity.ErrResultPending` | Return to complete activity asynchronously |

### Client APIs (`go.temporal.io/sdk/client`)

| API | Purpose |
|-----|---------|
| `client.Dial(options)` | Create a Temporal client |
| `c.ExecuteWorkflow(ctx, opts, fn, args...)` | Start a workflow |
| `c.GetWorkflow(ctx, workflowID, runID)` | Get handle to existing workflow |
| `c.CancelWorkflow(ctx, workflowID, runID)` | Request workflow cancellation |
| `c.TerminateWorkflow(ctx, workflowID, runID, reason)` | Force terminate |
| `c.SignalWorkflow(ctx, workflowID, runID, name, arg)` | Send signal |
| `c.QueryWorkflow(ctx, workflowID, runID, name, args...)` | Query workflow state |
| `c.CompleteActivity(ctx, taskToken, result, err)` | Async activity completion |
| `run.GetID()` | Get workflow ID from run |
| `run.Get(ctx, &result)` | Block until workflow completes |

### Worker & Testing APIs (`go.temporal.io/sdk/worker`, `go.temporal.io/sdk/testsuite`)

| API | Purpose |
|-----|---------|
| `worker.New(c, taskQueue, opts)` | Create a new worker |
| `w.RegisterWorkflow(fn)` | Register workflow function |
| `w.RegisterActivity(fn)` | Register activity function or struct |
| `w.Run(stopCh)` | Start worker (blocks until stop) |
| `testsuite.WorkflowTestSuite` | Embed in test struct for test environment |
| `env.ExecuteWorkflow(fn, args...)` | Run workflow in test environment |
| `env.OnActivity(fn, args...).Return(...)` | Mock activity return value |
| `env.RegisterDelayedCallback(d, fn)` | Trigger callback during test execution |
| `worker.NewWorkflowReplayer()` | Replay workflow history for debugging |

## Architecture

```
Application Code
      │  ExecuteWorkflow / SignalWorkflow / QueryWorkflow
      ▼
┌─────────────────────┐
│  Temporal Client     │  go.temporal.io/sdk/client
│  (SDK)               │
└────────┬────────────┘
         │  gRPC
         ▼
┌─────────────────────┐
│  Temporal Server     │  localhost:7233 / Temporal Cloud
│  (Service)           │
└────────┬────────────┘
         │  Task Queue polling
         ▼
┌─────────────────────┐
│  Worker              │  go.temporal.io/sdk/worker
│  (Hosts Workflows    │
│   & Activities)      │
└─────────────────────┘
```

## References

- [Core Application](references/core-application.md) — SDK installation, workflows, activities, workers, dynamic registration
- [Temporal Client](references/temporal-client.md) — Client creation, Cloud connection (mTLS/API keys), starting workflows
- [Namespaces](references/namespaces.md) — Register, update, describe, list, delete namespaces
- [Testing Suite](references/testing-suite.md) — TestWorkflowEnvironment, activity mocking, time skipping, replay
- [Failure Detection](references/failure-detection.md) — Timeouts, retry policies, heartbeats, custom retry delay
- [Cancellation](references/cancellation.md) — Workflow/activity cancellation patterns
- [Async Activity Completion](references/async-activity-completion.md) — External completion via task tokens
- [UI Metadata](references/ui-metadata.md) — StaticSummary, SetCurrentDetails, timer/activity summaries
- [Timers](references/timers.md) — Durable timers, workflow.Sleep, workflow.NewTimer
- [Debugging](references/debugging.md) — Deadlock detection, TEMPORAL_DEBUG, replay debugging
- [Continue-As-New](references/continue-as-new.md) — Event history management, state carryover
