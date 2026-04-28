# The Effect Type

## Contents
- The `Effect<A, E, R>` shape
- Laziness — descriptions vs executions
- Constructors
- Common combinators
- Reading signatures

## The shape

```ts
Effect<A, E, R>
```

- `A` — value produced on success
- `E` — typed expected error channel (defaults to `never` when there are no errors)
- `R` — required services (defaults to `never` when no DI is needed)

When `E = never` and `R = never`, the effect is fully self-contained and runnable.

## Laziness

An `Effect` is a **value** that describes a program. It does not execute when constructed — only when run. This is the single biggest mental shift from Promises. A `Promise` represents an *already-running* operation; an `Effect` is a recipe.

```ts
const x = Effect.sync(() => { console.log("hi"); return 1 })
// nothing logs yet
const a = await Effect.runPromise(x) // logs "hi", a = 1
const b = await Effect.runPromise(x) // logs "hi" again — same recipe, run twice
```

Implication: caching, memoization, and "run once" semantics need explicit primitives (`Effect.cached`, `Effect.memoize`).

## Constructors

| Need | Constructor | Notes |
|---|---|---|
| Pure value | `Effect.succeed(v)` | `Effect<V, never, never>` |
| Synchronous code | `Effect.sync(() => v)` | Defects if it throws |
| Synchronous code that may throw | `Effect.try({ try, catch })` | Throws → typed `E` |
| Promise (no error mapping) | `Effect.promise(() => p)` | Rejection becomes a defect |
| Promise (with error mapping) | `Effect.tryPromise({ try, catch })` | Rejection → typed `E` |
| Already failed | `Effect.fail(e)` | Adds `e` to `E` channel |
| Already a defect | `Effect.die(reason)` | Bug; bypasses `E` |
| Suspended (lazy) effect | `Effect.suspend(() => eff)` | Defer effect construction |
| From callback API | `Effect.async<A, E>((resume) => …)` | Must call `resume(Effect.succeed/fail)` once |

## Common combinators

```ts
Effect.map(eff, fn)            // transform success
Effect.flatMap(eff, fn)        // chain to next effect (fn returns Effect)
Effect.tap(eff, fn)            // run side effect, keep original A
Effect.zip(a, b)               // [A, B] — runs sequentially by default
Effect.zipRight(a, b)           // run a, then b, return B
Effect.all([a, b, c])           // tuple results; { concurrency: N } for parallel
Effect.forEach(items, fn)       // map + collect; supports concurrency option
Effect.match(eff, { onSuccess, onFailure })  // total handler — collapses E to never
```

## Reading signatures

The signature *is* the documentation. Train yourself to read left-to-right:

```ts
const charge: (
  cents: number
) => Effect<Receipt, CardDeclined | RateLimited, StripeClient | Logger>
```

Tells you exactly:
- Returns a `Receipt`
- May fail with `CardDeclined` or `RateLimited` (callers must handle or propagate)
- Needs `StripeClient` and `Logger` provided before it can run

If a function returns `Effect<X, never, never>`, it's pure-effectful and runnable anywhere — no errors to handle, no services to provide.

## See also

- [runtime-and-execution](runtime-and-execution.md) — how to actually run an Effect
- [error-handling](error-handling.md) — what goes in `E`
- [services-and-layers](services-and-layers.md) — what goes in `R`
