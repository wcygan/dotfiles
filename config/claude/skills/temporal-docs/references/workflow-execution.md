# Workflow Execution

Use this reference for Workflow Execution identity, status, replay, commands, events, execution chains, Continue-As-New, timers, limits, and Event History links.

## Sources

- Rendered: https://docs.temporal.io/workflow-execution
- Markdown: https://docs.temporal.io/workflow-execution.md
- Workflow ID and Run ID: https://docs.temporal.io/workflow-execution/workflowid-runid
- Events: https://docs.temporal.io/workflow-execution/event
- Continue-As-New: https://docs.temporal.io/workflow-execution/continue-as-new
- Limits: https://docs.temporal.io/workflow-execution/limits
- Timers and Start Delays: https://docs.temporal.io/workflow-execution/timers-delays

## Read For

- What a Workflow Execution is.
- Durability, reliability, and scalability of executions.
- Workflow Execution state and concurrency.
- Commands, Awaitables, Events, and Event History.
- Workflow Execution status and execution chains.
- Workflow ID vs Run ID.
- When Continue-As-New handles history growth or load.

## Current Hub Links

Inspect rendered HTML for current adjacency. Expected core links include:

- https://docs.temporal.io/workflow-execution/workflowid-runid
- https://docs.temporal.io/workflow-execution/event
- https://docs.temporal.io/workflow-execution/continue-as-new
- https://docs.temporal.io/workflow-execution/limits
- https://docs.temporal.io/workflow-execution/timers-delays
- https://docs.temporal.io/encyclopedia/event-history/

## Answering Guidance

Describe a Workflow Execution as the durable running unit of a Temporal Application. Connect replay to Event History: Commands from Worker code map to Events persisted by the Temporal Service, and Workers use those events to resume execution. Use the identity subpage for exact Workflow ID and Run ID semantics.
