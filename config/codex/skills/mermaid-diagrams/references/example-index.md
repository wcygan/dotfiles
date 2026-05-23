# Example Index

Use these examples as copyable starting points.

| File | Use |
| --- | --- |
| `examples/architecture-data-platform-icons.mmd` | Flowchart architecture map with Postgres, MySQL, Temporal, Kafka, Redis, TiDB, Flink, Spark, HDFS, and custom-icon placeholders for DragonflyDB and Redpanda. |
| `examples/flowchart-icon-data-stack.mmd` | Flowchart with Iconify icon-shaped nodes. |
| `examples/flowchart-cdc-pipeline.mmd` | CDC lane diagram with write path, change capture, read model, fallback read, and DLQ handling. |
| `examples/sequence-temporal-kafka.mmd` | Request, workflow activity, outbox relay, Kafka publish, and projection update sequence. |
| `examples/erd-commerce-events.mmd` | ERD for orders, payments, outbox events, and projections. |
| `examples/state-workflow-retries.mmd` | Workflow retry, compensation, completion, and failure lifecycle. |

## Copy Path

1. Copy the closest `.mmd` file.
2. Rename node IDs to match the target system.
3. Replace labels with concrete service, table, topic, task queue, and job names.
4. Render once in the target environment.
5. Trim nodes until every remaining node supports the story.
