# Temporal Service

Use this reference for Temporal Service architecture, server components, persistence, task routing, visibility, and Cloud vs self-hosted topology.

## Sources

- Rendered: https://docs.temporal.io/temporal-service
- Markdown: https://docs.temporal.io/temporal-service.md
- Temporal Platform overview: https://docs.temporal.io/temporal
- Workers: https://docs.temporal.io/workers
- Namespaces: https://docs.temporal.io/namespaces

## Read For

- What the Temporal Service does.
- Frontend, History, Matching, and Worker Service roles.
- Persistence and visibility stores.
- Task Queue matching and history ownership.
- Service boundaries relative to application Workers.
- Deployment architecture for Temporal Cloud or self-hosted clusters.

## Navigation Notes

- Use `/temporal-service` when the question is about server-side responsibilities.
- Use `/workers` when the question is about application process responsibilities.
- Use `/task-queue` when the question is about routing work to Workers.
- Use `/namespaces` when the question is about isolation and retention.

## Answering Guidance

Keep the Service/Worker boundary clear. The Temporal Service stores durable state, records Event History, schedules tasks, and exposes APIs. Workers run application Workflow and Activity code, poll Task Queues, and report completions back to the Service.
