# Debugging

**Source**: https://docs.temporal.io/develop/go/debugging

## Deadlock Detection

The Temporal Go SDK detects potential deadlocks in workflow code. If a workflow goroutine does not yield within 1 second (default), the SDK panics with a `PanicError`:

```
Potential deadlock detected: workflow goroutine "root" didn't yield for over 1s
```

### Common causes

| Cause | Fix |
|-------|-----|
| `time.Sleep()` in workflow | Use `workflow.Sleep()` |
| Blocking channel op (`<-ch`) | Use `workflow.NewChannel` + `workflow.Go` |
| `sync.Mutex.Lock()` in workflow | Remove; workflows are single-threaded |
| Infinite loop with no yield | Add `workflow.Sleep(ctx, 0)` or restructure |
| `go fn()` blocking the main routine | Use `workflow.Go(ctx, fn)` |
| Heavy computation (>1s CPU) | Move to an activity |

### Adjusting the deadlock timeout

Increase the threshold for legitimate long-running workflow tasks (rare):

```go
w := worker.New(c, "task-queue", worker.Options{
    DeadlockDetectionTimeout: 2 * time.Second,
})
```

## TEMPORAL_DEBUG Environment Variable

Set `TEMPORAL_DEBUG=true` to disable deadlock detection entirely during development:

```bash
TEMPORAL_DEBUG=true go run ./worker
```

**Warning**: Only use in development. Production deadlock detection catches real bugs.

## Logging

Use `workflow.GetLogger` for replay-safe logging (logs are suppressed during replay to avoid noise):

```go
func MyWorkflow(ctx workflow.Context) error {
    logger := workflow.GetLogger(ctx)
    logger.Info("Workflow started", "workflowID", workflow.GetInfo(ctx).WorkflowExecution.ID)

    // ... work ...

    logger.Info("Workflow completed")
    return nil
}
```

Activity logging uses standard `context`-based logging:

```go
func MyActivity(ctx context.Context) error {
    logger := activity.GetLogger(ctx)
    logger.Info("Activity started", "attempt", activity.GetInfo(ctx).Attempt)
    return nil
}
```

## Web UI Debugging

The Temporal Web UI (default: `localhost:8233`) provides:
- **Workflow list**: filter by status, workflow type, search attributes
- **Event history**: full timeline of all events in execution order
- **Pending activities**: see which activities are running or scheduled
- **Stack trace**: query live stack traces of running workflows

## CLI Debugging

```bash
# Show workflow execution details
temporal workflow show --workflow-id my-workflow-id

# Show workflow event history as JSON
temporal workflow show --workflow-id my-workflow-id --output json

# Query a running workflow
temporal workflow query --workflow-id my-workflow-id --type get-state

# List running workflows
temporal workflow list --query 'ExecutionStatus="Running"'

# Describe workflow
temporal workflow describe --workflow-id my-workflow-id
```

## Workflow Replay Debugging

Replay a workflow history locally to identify non-determinism issues:

```go
func replayWorkflow() {
    replayer := worker.NewWorkflowReplayer()
    replayer.RegisterWorkflow(MyWorkflow)

    // Load history from file (export from Web UI or CLI)
    err := replayer.ReplayWorkflowHistoryFromJSONFile(
        nil, // logger (nil = default)
        "testdata/workflow-history.json",
    )
    if err != nil {
        log.Fatal("Non-determinism detected:", err)
    }
    log.Println("Replay successful — no non-determinism found")
}
```

### Export history for replay

```bash
# Export workflow history to JSON
temporal workflow show \
    --workflow-id my-workflow-id \
    --output json > testdata/workflow-history.json
```

## Common Non-Determinism Errors

```
panic: workflowcheck: random
```
Fix: Use `workflow.SideEffect` for random values.

```
panic: workflowcheck: time.Now
```
Fix: Use `workflow.Now(ctx)` instead of `time.Now()`.

```
History mismatch: command type doesn't match
```
Fix: Don't add/remove/reorder `ExecuteActivity`, `Sleep`, or `Go` calls between versions — use `workflow.GetVersion` for safe upgrades.

## Workflow Versioning for Safe Upgrades

Use `workflow.GetVersion` to handle non-deterministic changes safely:

```go
func MyWorkflow(ctx workflow.Context) error {
    v := workflow.GetVersion(ctx, "my-feature", workflow.DefaultVersion, 1)

    if v == workflow.DefaultVersion {
        // Old behavior
        return workflow.ExecuteActivity(ctx, OldActivity).Get(ctx, nil)
    }

    // New behavior (v == 1)
    return workflow.ExecuteActivity(ctx, NewActivity).Get(ctx, nil)
}
```

## Tracing

The SDK supports OpenTelemetry tracing via interceptors:

```go
import "go.temporal.io/sdk/contrib/opentelemetry"

tracingInterceptor, err := opentelemetry.NewTracingInterceptor(opentelemetry.TracerOptions{
    Tracer: otel.Tracer("my-service"),
})

w := worker.New(c, "task-queue", worker.Options{
    Interceptors: []interceptor.WorkerInterceptor{tracingInterceptor},
})
```

## Metrics

Workers emit Prometheus-compatible metrics via `go.temporal.io/sdk/contrib/prometheus`:

```go
import "go.temporal.io/sdk/contrib/prometheus"

metricsHandler := prometheus.NewScopeHandler(prometheus.ScopeOptions{
    ListenAddress: "0.0.0.0:9090",
})

c, err := client.Dial(client.Options{
    MetricsHandler: metricsHandler,
})
```
