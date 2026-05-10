# Concurrency, Resources, and Scheduling

Use this when adding parallelism, cancellation, queues, pub/sub, resource cleanup, retry, repeat, polling, cron, or timeout behavior. Verify exact APIs in the official docs or installed package exports before editing.

Official docs to check first:
- https://effect.website/docs/concurrency/basic-concurrency/
- https://effect.website/docs/concurrency/fibers/
- https://effect.website/docs/concurrency/deferred/
- https://effect.website/docs/concurrency/queue/
- https://effect.website/docs/concurrency/pubsub/
- https://effect.website/docs/concurrency/semaphore/
- https://effect.website/docs/resource-management/introduction/
- https://effect.website/docs/resource-management/scope/
- https://effect.website/docs/scheduling/introduction/
- https://effect.website/docs/scheduling/built-in-schedules/
- https://effect.website/docs/scheduling/repetition/
- https://effect.website/docs/error-management/retrying/
- https://effect.website/docs/error-management/timing-out/

## Structured Concurrency

Prefer high-level combinators before raw fibers:

- Need all results: all/for-each style combinators with an explicit concurrency policy.
- Need first winner: race, then confirm what happens to losers.
- Need background work: fork under a scope, supervisor, or runtime lifecycle.
- Need coordination: Deferred, Queue, PubSub, Semaphore, Ref, or related state-management primitives.

Do not use unbounded concurrency by default. Make the concurrency limit visible when processing user data, network calls, or database work.

## Fibers and Cancellation

Every Effect runs on a fiber. Forked work should have an owner:

- Joined by the parent.
- Scoped to a resource lifetime.
- Supervised by the runtime.
- Explicitly detached only when that is the intended lifecycle.

When wrapping Promise APIs, remember that fiber interruption does not automatically cancel the underlying Promise unless the wrapped API supports cancellation, such as an AbortSignal-aware operation.

## Resource Safety

Use scoped resource management for anything that needs cleanup:

- DB connections and pools.
- File handles.
- Locks and semaphores.
- Servers, subscriptions, and telemetry exporters.
- Temporary directories or external processes.

Finalizers should run on success, failure, and interruption. Avoid manual `try/finally` around Effect programs unless the code is deliberately outside Effect.

## Retry, Repeat, and Timeout

Choose deliberately:

- Retry: repeat on failure until success or policy exhaustion.
- Repeat: repeat after success, often for polling.
- Timeout: interrupt work after a duration and route timeout as a typed outcome when the caller can recover.
- Cron/schedule: use when recurrence policy is part of the program, not just a shell or platform concern.

Retry only failures that are safe to retry. Avoid retrying validation errors, authorization errors, or non-idempotent operations without an idempotency key or compensating design.

## Code Review Checks

- Is concurrency bounded where external resources are involved?
- Are forked fibers joined, scoped, supervised, or intentionally detached?
- Do finalizers run on interruption?
- Is retry limited to transient/idempotent failures?
- Are timeout failures routed as domain outcomes when appropriate?
- Are exact schedule and concurrency options verified against current docs?
