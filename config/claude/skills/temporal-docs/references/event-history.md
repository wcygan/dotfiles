# Event History

Use this reference for Event History, Commands, replay, history growth, failure recovery, and how Temporal reconstructs Workflow state.

## Sources

- Rendered: https://docs.temporal.io/encyclopedia/event-history/
- Raw MDX: https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/event-history/event-history.mdx
- Events reference page: https://docs.temporal.io/workflow-execution/event
- Workflow Execution overview: https://docs.temporal.io/workflow-execution

## Read For

- What Event History records.
- How Commands become Events.
- How replay reconstructs Workflow state.
- Why Activity results are recorded and reused.
- Why large histories may require Continue-As-New.
- Where language-specific Event History walkthroughs live.

## Current Hub Links

Expected links from the Event History page include:

- https://docs.temporal.io/workflow-execution/event
- https://docs.temporal.io/encyclopedia/event-history/event-history-go
- https://docs.temporal.io/encyclopedia/event-history/event-history-java
- https://docs.temporal.io/encyclopedia/event-history/event-history-python
- https://docs.temporal.io/encyclopedia/event-history/event-history-typescript
- https://docs.temporal.io/encyclopedia/event-history/event-history-dotnet

## Answering Guidance

Describe Event History as the durable ordered log that lets Temporal recreate Workflow state after process failure. Tie it to replay and determinism. When the user asks for exact event names or lifecycle sequences, read `/workflow-execution/event` and the relevant SDK walkthrough.
