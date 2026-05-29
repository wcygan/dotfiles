# Child Workflows

Use this reference for Child Workflow Executions, parent-child lifecycle, parent close policy, cancellation, and decomposition boundaries.

## Sources

- Rendered: https://docs.temporal.io/child-workflows
- Markdown: https://docs.temporal.io/child-workflows.md
- Workflow Execution: https://docs.temporal.io/workflow-execution
- Workflow message passing: https://docs.temporal.io/encyclopedia/workflow-message-passing/

## Read For

- When one Workflow should start another.
- Parent Close Policy behavior.
- Child Workflow cancellation and termination relationships.
- Workflow decomposition into independently tracked executions.
- How Child Workflows differ from Activities.

## Navigation Notes

- Start with `/child-workflows` for the concept.
- Follow SDK-specific child Workflow pages only when code syntax matters.
- Follow `/workflow-execution` for identity, execution chain, and Event History context.

## Answering Guidance

Explain Child Workflows as separate Workflow Executions started by a parent Workflow. Use them when the child needs its own durable lifecycle, identity, history, retries, visibility, or cancellation policy. Prefer Activities for one bounded unit of external work.
