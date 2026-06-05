# Temporal Python SDK Documentation Map

Checked: 2026-06-05
Source: https://docs.temporal.io/develop/python/
Scope: `/develop/python/`

Use this map to choose the smallest official page to read before answering or editing code.

## Start Here

- Python SDK developer guide: https://docs.temporal.io/develop/python/
  - Hub for Workflows, Activities, Workers, Client, Nexus, Platform, best practices, integrations, API docs, and samples.
- Quickstart: https://docs.temporal.io/develop/python/set-up-your-local-python
  - Install `temporalio`, install Temporal CLI, start `temporal server start-dev`, and run a minimal Workflow/Activity/Worker app.
- Temporal Client: https://docs.temporal.io/develop/python/client/temporal-client
  - Connect to local dev or Temporal Cloud, start Workflows, get results, and load connection config from env, TOML, or code.

## Core Application Pieces

- Workflow basics: https://docs.temporal.io/develop/python/workflows/basics
  - `@workflow.defn`, `@workflow.run`, Workflow parameters, return values, custom Workflow names, and deterministic import patterns.
- Activity basics: https://docs.temporal.io/develop/python/activities/basics
  - `@activity.defn`, Activity parameters and return values, payload size considerations, and implementation shapes.
- Worker processes: https://docs.temporal.io/develop/python/workers/run-worker-process
  - `Worker(...)`, Task Queue registration, Workflow and Activity type lists, and same-type registration rules for Workers polling one Task Queue.
- Temporal Client: https://docs.temporal.io/develop/python/client/temporal-client
  - Client creation, local and Cloud connection options, Workflow start/result APIs, Signals, Queries, and Updates.

## Workflow Features

- Workflow message passing: https://docs.temporal.io/develop/python/workflows/message-passing
  - Query, Signal, and Update decorators, handler constraints, async handlers, validators, and client interaction.
- Schedules: https://docs.temporal.io/develop/python/workflows/schedules
  - Create, backfill, delete, describe, list, pause, trigger, and update scheduled Workflows. Prefer Schedules over Cron Jobs.
- Versioning: https://docs.temporal.io/develop/python/workflows/versioning
  - Determinism-safe changes with Worker Versioning or patching.
- Continue-As-New: https://docs.temporal.io/develop/python/workflows/continue-as-new
  - Rollover for long-running Workflows and large Event Histories.
- Workflow Streams: https://docs.temporal.io/develop/python/workflows/workflow-streams
  - Durable offset-addressed event channels built on Signals, Updates, and Queries. Read `workflow-streams-llm.md` for LLM output streaming.

## Best Practices

- Error handling: https://docs.temporal.io/develop/python/best-practices/error-handling
  - Idempotent Activities, `ApplicationError`, retry policies, non-retryable errors, Saga rollback, and failure types.
- Testing: https://docs.temporal.io/develop/python/best-practices/testing-suite
  - End-to-end, integration, and unit testing; prefer integration tests for most Temporal behavior.
- Python SDK sandbox: https://docs.temporal.io/develop/python/best-practices/python-sdk-sandbox
  - Workflow sandboxing, passthrough modules, restrictions, determinism protection, and escape hatches.
- Sync vs async Activities: https://docs.temporal.io/develop/python/best-practices/python-sdk-sync-vs-async
  - Worker execution architecture and how to avoid blocking the async event loop.

## Data, Security, And Operations

- Payload conversion: https://docs.temporal.io/develop/python/data-handling/data-conversion
  - Default converter behavior, dataclasses, Pydantic converter, custom payload converters, and compatibility considerations.
- Payload encryption: https://docs.temporal.io/develop/python/data-handling/data-encryption
  - Payload Codecs, encryption/compression, Data Converter configuration, and Codec Server support.
- Observability: https://docs.temporal.io/develop/python/platform/observability
  - SDK metrics, Prometheus, OpenTelemetry tracing, Workflow logging, and Visibility APIs.

## Notes

- Workflow Streams is in Public Preview and currently has Python client support; verify the current page before relying on API stability.
- Use `temporal-docs` for platform concepts such as Event History, Task Queues, durable execution, and determinism when language APIs are not the main task.
