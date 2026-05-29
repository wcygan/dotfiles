# Detecting Application Failures

Use this reference for high-level failure boundaries, retry behavior, timeouts, heartbeats, and how Temporal detects Activity and Workflow failures.

## Sources

- Rendered: https://docs.temporal.io/encyclopedia/detecting-application-failures
- Markdown: https://docs.temporal.io/encyclopedia/detecting-application-failures.md
- Activity failure detection: https://docs.temporal.io/encyclopedia/detecting-activity-failures
- Workflow failure detection: https://docs.temporal.io/encyclopedia/detecting-workflow-failures

## Read For

- How Temporal detects failures in application code.
- Activity timeout types and retries.
- Heartbeat timeout and heartbeat details.
- Workflow Execution timeout, Run timeout, and Task timeout.
- When failures are retried vs surfaced to Workflow code.
- How failure detection connects to Event History.

## Navigation Notes

- Start with `/encyclopedia/detecting-application-failures` for the overview.
- Follow Activity-specific pages for Start-To-Close, Schedule-To-Close, Schedule-To-Start, heartbeat timeout, retries, and cancellation delivery.
- Follow Workflow-specific pages for Workflow Execution timeout, Workflow Run timeout, Workflow Task timeout, and retry policies.

## Answering Guidance

Frame failures by execution type. Activities are expected to fail and retry around external work. Workflows are expected to preserve durable state and continue across process failures, while Workflow Task failures usually indicate code or determinism issues that must be fixed.
