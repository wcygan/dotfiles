# Testing Suite

**Source**: https://docs.temporal.io/develop/go/testing-suite

## Overview

The Temporal Go SDK provides `go.temporal.io/sdk/testsuite` for unit testing workflows and activities without a running Temporal server. The test environment handles determinism, time skipping, and activity mocking.

## Setup

```go
import (
    "testing"
    "github.com/stretchr/testify/suite"
    "go.temporal.io/sdk/testsuite"
)

type UnitTestSuite struct {
    suite.Suite
    testsuite.WorkflowTestSuite
    env *testsuite.TestWorkflowEnvironment
}

func (s *UnitTestSuite) SetupTest() {
    s.env = s.NewTestWorkflowEnvironment()
}

func (s *UnitTestSuite) AfterTest(suiteName, testName string) {
    s.env.AssertExpectations(s.T())
}

func TestUnitTestSuite(t *testing.T) {
    suite.Run(t, new(UnitTestSuite))
}
```

## Executing a Workflow

```go
func (s *UnitTestSuite) Test_SimpleWorkflow() {
    s.env.ExecuteWorkflow(TransferMoneyWorkflow, TransferInput{
        FromAccount: "A",
        ToAccount:   "B",
        Amount:      100.0,
    })

    s.True(s.env.IsWorkflowCompleted())
    s.NoError(s.env.GetWorkflowError())

    var result TransferResult
    s.NoError(s.env.GetWorkflowResult(&result))
    s.Equal("completed", result.Status)
}
```

## Mocking Activities

### Fixed return value

```go
func (s *UnitTestSuite) Test_WithMockedActivity() {
    s.env.OnActivity(WithdrawActivity, mock.Anything, mock.Anything).
        Return(nil)  // success

    s.env.OnActivity(DepositActivity, mock.Anything, mock.Anything).
        Return(nil)

    s.env.ExecuteWorkflow(TransferMoneyWorkflow, input)
    s.True(s.env.IsWorkflowCompleted())
    s.NoError(s.env.GetWorkflowError())
}
```

### Return an error

```go
s.env.OnActivity(WithdrawActivity, mock.Anything, mock.Anything).
    Return(temporal.NewApplicationError("insufficient funds", "InsufficientFunds"))
```

### Custom implementation override

```go
s.env.OnActivity(SendEmailActivity, mock.Anything, "user@example.com").
    Return(func(ctx context.Context, email string) error {
        // custom logic for test
        return nil
    })
```

### Call through to real implementation

```go
s.env.OnActivity(ValidateActivity, mock.Anything, mock.Anything).
    Return(func(ctx context.Context, input string) (bool, error) {
        // execute real implementation
        return realValidateActivity(ctx, input)
    })
```

### Using mock.MatchedBy for argument matching

```go
s.env.OnActivity(ProcessActivity, mock.Anything,
    mock.MatchedBy(func(req ProcessRequest) bool {
        return req.Amount > 0
    }),
).Return(ProcessResult{Success: true}, nil)
```

## Testing Signals and Queries

### Sending a signal during test

```go
func (s *UnitTestSuite) Test_WorkflowWithSignal() {
    s.env.RegisterDelayedCallback(func() {
        s.env.SignalWorkflow("my-signal", "signal-payload")
    }, time.Second*5)

    s.env.ExecuteWorkflow(SignalHandlerWorkflow)
    s.True(s.env.IsWorkflowCompleted())
}
```

### Querying workflow state

```go
func (s *UnitTestSuite) Test_QueryDuringExecution() {
    s.env.RegisterDelayedCallback(func() {
        val, err := s.env.QueryWorkflow("get-state")
        s.NoError(err)
        var state string
        val.Get(&state)
        s.Equal("processing", state)
    }, time.Second*2)

    s.env.ExecuteWorkflow(MyStatefulWorkflow)
}
```

## Time Skipping

The test environment automatically skips time when the workflow is blocked (e.g., waiting on `workflow.Sleep`). You can also manually control time:

```go
func (s *UnitTestSuite) Test_TimerWorkflow() {
    // This workflow sleeps for 24 hours
    s.env.ExecuteWorkflow(DailyCleanupWorkflow)

    // Time was automatically skipped — test completes instantly
    s.True(s.env.IsWorkflowCompleted())
    s.NoError(s.env.GetWorkflowError())
}
```

### Register callback before specific delay

```go
s.env.RegisterDelayedCallback(func() {
    // Called when simulated time reaches 1 hour
    s.env.SignalWorkflow("check-status", nil)
}, time.Hour)
```

## Testing Activity Heartbeats

```go
func (s *UnitTestSuite) Test_ActivityWithHeartbeat() {
    s.env.OnActivity(LongRunningActivity, mock.Anything, mock.Anything).
        Return(func(ctx context.Context, input string) error {
            activity.RecordHeartbeat(ctx, "checkpoint-1")
            return nil
        })

    s.env.ExecuteWorkflow(MyWorkflow, "input")
    s.True(s.env.IsWorkflowCompleted())
}
```

## Nexus Operation Mocking

### Synchronous Nexus mock

```go
s.env.OnNexusOperation(myService, myOperation, mock.Anything, mock.Anything).
    Return(&nexus.HandlerStartOperationResultSync[MyOutput]{
        Value: &MyOutput{Result: "done"},
    }, nil)
```

### Asynchronous Nexus mock

```go
s.env.OnNexusOperation(myService, myOperation, mock.Anything, mock.Anything).
    Return(&nexus.HandlerStartOperationResultAsync{
        OperationID: "op-123",
    }, nil)

s.env.RegisterDelayedCallback(func() {
    s.env.CompleteNexusOperation("op-123", &MyOutput{Result: "done"}, nil)
}, time.Second)
```

## Workflow Replay Testing

Use `worker.NewWorkflowReplayer()` to validate that new workflow code is backward-compatible with existing history:

```go
func Test_ReplayWorkflow(t *testing.T) {
    replayer := worker.NewWorkflowReplayer()
    replayer.RegisterWorkflow(TransferMoneyWorkflow)

    // Load a real workflow history from file (JSON format from Web UI / CLI export)
    err := replayer.ReplayWorkflowHistoryFromJSONFile(nil, "testdata/workflow-history.json")
    require.NoError(t, err, "Replay failed — non-determinism change detected")
}
```

### Exporting history for replay tests

```bash
# Export via Temporal CLI
temporal workflow show --workflow-id my-workflow-id --output json > testdata/workflow-history.json
```

## Test Timeout

By default tests have no timeout. Add context timeout to prevent hanging:

```go
func (s *UnitTestSuite) SetupTest() {
    s.env = s.NewTestWorkflowEnvironment()
    s.env.SetTestTimeout(time.Second * 30)
}
```

## Activity Test Suite

For testing activities in isolation (real context, not mocked):

```go
type ActivityUnitTestSuite struct {
    suite.Suite
    testsuite.WorkflowTestSuite
}

func (s *ActivityUnitTestSuite) Test_EmailActivity() {
    env := s.NewTestActivityEnvironment()
    env.RegisterActivity(EmailActivity)

    val, err := env.ExecuteActivity(EmailActivity, "user@example.com")
    s.NoError(err)

    var result bool
    val.Get(&result)
    s.True(result)
}
```
