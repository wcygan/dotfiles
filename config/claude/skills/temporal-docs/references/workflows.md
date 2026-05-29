# Workflows

Use this reference for Workflow concepts, replay, determinism, Workflow Definition vs Workflow Execution, and what code belongs in Workflows.

## Sources

- Rendered: https://docs.temporal.io/workflows
- Markdown: https://docs.temporal.io/workflows.md
- Workflow Definition: https://docs.temporal.io/workflow-definition
- Workflow Execution: https://docs.temporal.io/workflow-execution

## Read For

- What "Workflow" means in conversation.
- Workflow Definition, Workflow Type, and Workflow Execution distinctions.
- Durable, long-running, resilient execution.
- Replay and deterministic constraints.
- Why side effects belong in Activities.
- Which pages `/workflows` links to.

## Current Hub Links

The `/workflows` page is a hub. Inspect live HTML before answering adjacency questions. Expected core links include:

- https://docs.temporal.io/workflow-definition
- https://docs.temporal.io/workflow-execution
- https://docs.temporal.io/schedule
- https://docs.temporal.io/dynamic-handler
- https://docs.temporal.io/cron-job

## Answering Guidance

Start with the three-term split:

- Workflow Definition: code that defines the workflow.
- Workflow Type: name that maps to a definition.
- Workflow Execution: one durable running instance.

Then explain replay: Temporal rebuilds Workflow state from Event History and recorded results, so Workflow code must make the same decisions when replaying the same history. Point side effects, external I/O, slow calls, and non-deterministic work toward Activities.
