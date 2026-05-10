# Errors and Runtime Boundaries

Use this when modeling errors, recovering from failures, routing HTTP responses, logging causes, or deciding how a framework boundary should run an Effect program. Verify exact APIs in the official docs or installed package exports before editing.

Official docs to check first:
- https://effect.website/docs/error-management/two-error-types/
- https://effect.website/docs/error-management/expected-errors/
- https://effect.website/docs/error-management/unexpected-errors/
- https://effect.website/docs/error-management/error-channel-operations/
- https://effect.website/docs/error-management/matching/
- https://effect.website/docs/error-management/sandboxing/
- https://effect.website/docs/error-management/yieldable-errors/
- https://effect.website/docs/data-types/cause/
- https://effect.website/docs/data-types/exit/
- https://effect.website/docs/getting-started/running-effects/

## Failure vs Defect

Effect distinguishes expected failures from unexpected defects:

- Failure: typed in `E`, recoverable, part of domain/control flow.
- Defect: untyped bug or impossible state, tracked by the runtime but not part of `E`.
- Interruption: cancellation, also represented in causes.

Rule of thumb: if a caller can reasonably respond to it, put it in `E`. If it means the program is wrong, make it a defect or let it surface as one.

## Tagged Domain Errors

Prefer tagged domain errors when callers need precise recovery:

```ts
class UserNotFound extends Data.TaggedError("UserNotFound")<{
  readonly id: string
}> {}
```

Benefits:

- A stable `_tag` for pattern matching and targeted recovery.
- Error-specific fields without parsing messages.
- Type narrowing as handlers recover specific tags.

Verify current tagged-error and yieldable-error idioms before adding new error classes; Effect has evolved in this area.

## Wrapping Unsafe Code

When wrapping thrown or rejecting APIs:

- Map expected failures into your domain errors.
- Preserve original causes when useful for logs or diagnostics.
- Do not let expected operational errors become defects by accident.
- Keep callback or Promise cancellation behavior explicit; wrapping a Promise does not make its underlying work cancellable unless the producer supports cancellation.

## Runtime Edge Pattern

At a framework boundary:

1. Decode or validate external input.
2. Build the Effect program in domain code.
3. Provide required services.
4. Add span/log annotations if the project uses observability.
5. Run at the edge.
6. Route success, typed failures, defects, and interruptions deliberately.

Prefer an exit-returning runner when the edge must distinguish domain failures from defects. Log pretty causes for defects and unexpected failures, but do not leak internal details in user-facing responses.

## Recovery Choices

Use targeted recovery first:

- Recover one tag when the fallback is specific.
- Recover multiple tags when producing the same boundary response.
- Use catch-all failure recovery only when the result is truly total.
- Use cause-level recovery sparingly; it can handle defects and interruption, so it should be deliberate.
- Use Either/Option conversions at boundaries when the success channel should carry absence or failure as data.

## Code Review Checks

- Are expected errors represented in `E`?
- Are defects reserved for bugs or impossible states?
- Does the HTTP/CLI/job boundary treat failures and defects differently?
- Are error tags stable and domain-specific?
- Are original thrown values preserved enough for diagnostics?
- Are exact recovery helper names verified against the local Effect version?
