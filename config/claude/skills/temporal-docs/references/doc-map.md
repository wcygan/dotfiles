# Temporal Docs Map

Checked: 2026-05-24

Use this map to choose the smallest official Temporal source before explaining or reviewing a general Temporal concept. Fetch the live page before relying on exact wording, page adjacency, or links.

## Primary Concept Pages

| Topic | Rendered docs | Markdown or source |
| --- | --- | --- |
| Temporal Platform | https://docs.temporal.io/temporal | https://docs.temporal.io/temporal.md |
| Workflows | https://docs.temporal.io/workflows | https://docs.temporal.io/workflows.md |
| Workflow Definition | https://docs.temporal.io/workflow-definition | https://docs.temporal.io/workflow-definition.md |
| Workflow Execution | https://docs.temporal.io/workflow-execution | https://docs.temporal.io/workflow-execution.md |
| Activities | https://docs.temporal.io/activities | https://docs.temporal.io/activities.md |
| Detecting application failures | https://docs.temporal.io/encyclopedia/detecting-application-failures | https://docs.temporal.io/encyclopedia/detecting-application-failures.md |
| Workers | https://docs.temporal.io/workers | https://docs.temporal.io/workers.md |
| Event History | https://docs.temporal.io/encyclopedia/event-history/ | https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/event-history/event-history.mdx |
| Workflow message passing | https://docs.temporal.io/encyclopedia/workflow-message-passing/ | https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/workflow-message-passing/workflow-message-passing.mdx |
| Child Workflows | https://docs.temporal.io/child-workflows | https://docs.temporal.io/child-workflows.md |
| Temporal Service | https://docs.temporal.io/temporal-service | https://docs.temporal.io/temporal-service.md |
| Namespaces | https://docs.temporal.io/namespaces | https://docs.temporal.io/namespaces.md |

## Workflow Execution Subpages

- Workflow ID and Run ID: https://docs.temporal.io/workflow-execution/workflowid-runid
- Events: https://docs.temporal.io/workflow-execution/event
- Continue-As-New: https://docs.temporal.io/workflow-execution/continue-as-new
- Limits: https://docs.temporal.io/workflow-execution/limits
- Timers and Start Delays: https://docs.temporal.io/workflow-execution/timers-delays

## Activity Subpages

- Activity Definition: https://docs.temporal.io/activity-definition
- Activity Execution: https://docs.temporal.io/activity-execution
- Activity operations: https://docs.temporal.io/activity-operations
- Local Activity: https://docs.temporal.io/local-activity
- Standalone Activity: https://docs.temporal.io/standalone-activity
- Detecting Activity failures: https://docs.temporal.io/encyclopedia/detecting-activity-failures

## Worker And Task Subpages

- Task Queues: https://docs.temporal.io/task-queue
- Tasks: https://docs.temporal.io/tasks
- Worker performance: https://docs.temporal.io/develop/worker-performance
- Worker tuning reference: https://docs.temporal.io/develop/worker-tuning-reference
- Worker Versioning: https://docs.temporal.io/worker-versioning

## Message Passing Subpages

- Sending messages: https://docs.temporal.io/sending-messages
- Handling messages: https://docs.temporal.io/handling-messages
- Signals: https://docs.temporal.io/sending-messages#sending-signals
- Queries: https://docs.temporal.io/handling-messages#queries
- Updates: https://docs.temporal.io/handling-messages#updates

## Routing Heuristics

- For "what is Temporal" or architecture questions, read `temporal-platform.md`.
- For durable execution, replay, determinism, and what code belongs in Workflow vs Activity, read `workflows.md`, `workflow-execution.md`, and `activities.md`.
- For identifiers, status, events, Continue-As-New, history size, timers, or execution chains, read `workflow-execution.md`.
- For retries, timeouts, heartbeat details, and failure boundaries, read `application-failures.md` plus `activities.md` or `workflow-execution.md`.
- For operational process layout, task queues, polling, or worker terminology, read `workers.md`.
- For Signals, Queries, Updates, and handler design, read `workflow-message-passing.md`.
- For decomposition into child executions, parent close policy, or cancellation propagation, read `child-workflows.md`.
- For cluster/service components, persistence, matching, history, and visibility, read `temporal-service.md`.
- For tenancy, retention, isolation, or environment boundaries, read `namespaces.md`.
