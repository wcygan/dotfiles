# Temporal Platform

Use this reference for high-level Temporal architecture, the distinction between the Temporal Platform and an application, and how Service, Workers, and SDKs fit together.

## Sources

- Rendered: https://docs.temporal.io/temporal
- Markdown: https://docs.temporal.io/temporal.md
- Adjacent: https://docs.temporal.io/temporal-service
- Adjacent: https://docs.temporal.io/workers
- Adjacent: https://docs.temporal.io/namespaces

## Read For

- "What is Temporal?"
- Durable execution as a platform model.
- Temporal Application boundaries.
- Temporal Service vs Worker vs SDK roles.
- Component topology and data flow.
- Which part is hosted by Temporal Cloud or self-hosted.

## Navigation Notes

- Start at `/temporal` for the platform overview.
- Follow `/temporal-service` for server-side components such as Frontend, History, Matching, Worker Service, persistence, and visibility.
- Follow `/workers` for the application-owned processes that execute Workflow and Activity code.
- Follow `/namespaces` for isolation and operational boundaries.

## Answering Guidance

Explain Temporal as a system for durable execution: application code runs in Workers, progress and history are coordinated by the Temporal Service, and SDKs provide the APIs for starting, running, and communicating with executions. Use the docs terms directly when distinguishing Temporal Platform, Temporal Service, Temporal Application, Workflow Execution, and Worker.
