# Activities

Use this reference for Activity concepts, Activity Definition vs Activity Execution, idempotency, Local Activities, Standalone Activities, heartbeat checkpointing, and failure boundaries.

## Sources

- Rendered: https://docs.temporal.io/activities
- Markdown: https://docs.temporal.io/activities.md
- Activity Definition: https://docs.temporal.io/activity-definition
- Activity Execution: https://docs.temporal.io/activity-execution
- Local Activity: https://docs.temporal.io/local-activity
- Standalone Activity: https://docs.temporal.io/standalone-activity
- Activity failure detection: https://docs.temporal.io/encyclopedia/detecting-activity-failures

## Read For

- What an Activity is.
- How Activities differ from Workflow code.
- Idempotency and retry-safe design.
- How Activity results enter Event History.
- Heartbeats and checkpointing.
- When a Standalone Activity is appropriate.
- How to split large work into multiple Activities.

## Current Hub Links

Expected core links from `/activities` include:

- https://docs.temporal.io/activity-definition
- https://docs.temporal.io/activity-execution
- https://docs.temporal.io/local-activity
- https://docs.temporal.io/standalone-activity
- https://docs.temporal.io/workflow-execution/event#activity-events

## Answering Guidance

Explain Activities as normal functions or methods that perform one well-defined action and can safely do non-deterministic work such as network calls, database access, file I/O, or LLM calls. Emphasize idempotency because retries may run an Activity attempt again after failure.
