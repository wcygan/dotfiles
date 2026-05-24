# Workflow Message Passing

Use this reference for Signals, Queries, Updates, handlers, validators, message ordering, and choosing the right message type.

## Sources

- Rendered: https://docs.temporal.io/encyclopedia/workflow-message-passing/
- Raw MDX: https://raw.githubusercontent.com/temporalio/documentation/main/docs/encyclopedia/workflow-message-passing/workflow-message-passing.mdx
- Sending messages: https://docs.temporal.io/sending-messages
- Handling messages: https://docs.temporal.io/handling-messages
- Event History: https://docs.temporal.io/workflow-execution/event#event-history

## Read For

- Signals vs Queries vs Updates.
- Async writes, synchronous tracked writes, and reads.
- Update validation and accepted/rejected Updates.
- Handler design and concurrency concerns.
- Limits for per-Workflow Updates.
- Message passing between clients and Workflow Executions.

## Current Hub Links

Expected links from the page include:

- https://docs.temporal.io/sending-messages
- https://docs.temporal.io/handling-messages
- https://docs.temporal.io/child-workflows
- https://docs.temporal.io/cloud/limits#per-workflow-execution-update-limits
- https://docs.temporal.io/workflow-execution/event#event-history

## Answering Guidance

Use this default distinction:

- Query: read current Workflow state without writing Event History.
- Signal: asynchronous write where the sender moves on without a result.
- Update: synchronous tracked write where the sender can wait for validation, completion, or failure.

For read-after-condition behavior, compare polling with Queries against an Update that can wait but records history.
