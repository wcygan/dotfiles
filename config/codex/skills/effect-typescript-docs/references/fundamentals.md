# Fundamentals

Use this when the task involves basic Effect design, reading signatures, choosing syntax style, or deciding where effects should run. Verify exact APIs in the official docs or the installed package before relying on signatures.

Official docs to check first:
- https://effect.website/docs/getting-started/the-effect-type/
- https://effect.website/docs/getting-started/creating-effects/
- https://effect.website/docs/getting-started/running-effects/
- https://effect.website/docs/getting-started/using-generators/
- https://effect.website/docs/getting-started/building-pipelines/
- https://effect.website/docs/code-style/guidelines/

## Mental Model

`Effect.Effect<A, E, R>` describes a program:

- `A`: success value.
- `E`: expected recoverable failure.
- `R`: services the program needs from its environment.

Effects are lazy. Creating an effect does not execute it; the runtime executes it later. This is the main difference from a `Promise`, which usually starts work as soon as it is created.

Read signatures as contracts:

```ts
const charge = (
  cents: number
): Effect.Effect<Receipt, CardDeclined | RateLimited, StripeClient | Logger>
```

That function returns a `Receipt`, can fail with two expected errors, and needs `StripeClient` plus `Logger` before it can run. At an application edge, the remaining `R` should usually be `never`.

## Constructors

Common choices:

- Pure value: `Effect.succeed(value)`.
- Synchronous side effect that should not throw: `Effect.sync(() => value)`.
- Synchronous API that may throw: wrap it with a failure-mapping constructor.
- Promise API that may reject: wrap it with a failure-mapping Promise constructor.
- Domain failure already in hand: `Effect.fail(error)`.
- Bug or impossible state: defect/die path, not a recoverable domain failure.
- Callback API: async bridge, with cancellation semantics checked carefully.

Before writing exact code, verify the constructor shape in official docs or installed exports because overloads and helper names are the part most likely to drift.

## Syntax Style

Default to `Effect.gen` for multi-step business logic:

```ts
const program = Effect.gen(function* () {
  const user = yield* loadUser(id)
  const receipt = yield* chargeUser(user)
  return receipt
})
```

Use `pipe` for short transformations, recovery chains, and declarative assembly:

```ts
const program = loadUser(id).pipe(
  Effect.flatMap(chargeUser),
  Effect.catchTag("UserNotFound", handleMissingUser)
)
```

Mix styles when it improves readability. Do not contort a sequential workflow into a long nested pipeline.

## Running Effects

Run once at the edge:

- HTTP handler.
- CLI main.
- Worker or scheduled job entry.
- Test harness.
- Framework adapter.

Avoid `runPromise` or `runSync` inside domain logic. Crossing back to `Promise` too early hides `E` and `R`, weakens testability, and often leads to repeated layer/runtime construction.

Choose the runner by boundary:

- Promise boundary: async runner.
- Need to inspect structured failure/defect causes: exit-returning runner.
- Truly synchronous script or test: sync runner.
- Background fiber that will be supervised or joined later: fork runner.

## Code Review Checks

- Does the code preserve `E` instead of throwing or returning nullable values?
- Does the code preserve `R` until the boundary instead of using globals?
- Is `Effect.gen` used where it makes sequential logic readable?
- Are effects run at the boundary, not inside helpers?
- Are exact API names verified against the local Effect version?
