# Workers

Use this reference for Worker terminology, Task Queues, polling, Worker Processes, Worker Entities, Worker Identity, cache behavior, and worker tuning entry points.

## Sources

- Rendered: https://docs.temporal.io/workers
- Markdown: https://docs.temporal.io/workers.md
- Task Queues: https://docs.temporal.io/task-queue
- Tasks: https://docs.temporal.io/tasks
- Worker performance: https://docs.temporal.io/develop/worker-performance
- Worker tuning reference: https://docs.temporal.io/develop/worker-tuning-reference

## Read For

- Worker Program vs Worker Process vs Worker Entity.
- Worker Identity and debugging.
- How Workers poll Task Queues.
- Workflow Worker and Activity Worker roles.
- Why Workers can be stateless while Workflow state is durable.
- Operational tuning and poller visibility.

## Current Hub Links

Expected concept links include:

- https://docs.temporal.io/task-queue
- https://docs.temporal.io/tasks
- https://docs.temporal.io/temporal-service
- https://docs.temporal.io/develop/worker-performance
- https://docs.temporal.io/develop/worker-tuning-reference

## Answering Guidance

Use precise Worker terms. A Worker Program is the static code. A Worker Process is a running process. A Worker Entity is an individual worker inside a process that listens on one Task Queue. Explain that the Temporal Service stores durable history; Workers poll, execute, and report progress.
