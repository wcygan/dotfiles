# Namespaces

Use this reference for Namespace concepts, isolation, retention, archival, endpoint scoping, and operational boundaries.

## Sources

- Rendered: https://docs.temporal.io/namespaces
- Markdown: https://docs.temporal.io/namespaces.md
- Temporal Service: https://docs.temporal.io/temporal-service
- Temporal Platform: https://docs.temporal.io/temporal

## Read For

- What a Namespace is.
- Why Namespaces isolate Workflow Executions.
- Retention period and archival behavior.
- Registration and naming.
- Operational environment boundaries such as dev, staging, production, or tenants.
- Cloud vs self-hosted namespace considerations.

## Navigation Notes

- Start with `/namespaces` for concept semantics.
- Follow Temporal Cloud docs for Cloud-specific Namespace management and account boundaries.
- Follow CLI docs only when the user needs exact commands to register, describe, or update a Namespace.

## Answering Guidance

Explain Namespaces as logical isolation boundaries inside Temporal. Use them to scope Workflow IDs, retention, visibility, and operational controls. Recommend environment or tenant boundaries only after considering visibility, retention, access control, and operational ownership.
