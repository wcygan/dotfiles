# Fibers and Structured Concurrency

## Contents
- What a fiber is
- Forking and joining
- Combinators: `all`, `race`, `forEach`
- Interruption and cancellation
- Supervision
- Common pitfalls

## What a fiber is

A **fiber** is a lightweight virtual thread cooperatively scheduled on the JS event loop. Every Effect runs on a fiber. Fibers can:

- Be forked to run concurrently
- Be interrupted (cancelled) — interruption propagates structurally to children
- Have their result observed via `Fiber.join` (blocking) or `Fiber.await` (returns `Exit`)
- Carry a `FiberRef` (fiber-local state, like AsyncLocalStorage with structure)

Unlike Promises, fibers give you **structured concurrency**: a forked child belongs to a parent scope, and when the parent ends, children are interrupted automatically.

## Forking and joining

```ts
import { Effect, Fiber } from "effect"

const program = Effect.gen(function* () {
  const fiberA = yield* Effect.fork(longJobA)
  const fiberB = yield* Effect.fork(longJobB)
  const a = yield* Fiber.join(fiberA)
  const b = yield* Fiber.join(fiberB)
  return [a, b]
})
```

`Effect.fork` produces an `Effect<RuntimeFiber<A, E>>`. The fiber starts running immediately. When the parent fiber ends (success, failure, or interrupt), unjoinedjoined children are interrupted.

## Combinators

You rarely need raw `fork`/`join`. Prefer:

```ts
// All complete; tuple result; sequential by default
Effect.all([a, b, c])

// Parallel up to N at a time (-1 = unlimited)
Effect.all([a, b, c], { concurrency: 5 })

// First to succeed wins; losers are interrupted
Effect.race(a, b)

// First to complete (success or failure) wins
Effect.raceAll([a, b, c])

// forEach with concurrency
Effect.forEach(items, fn, { concurrency: 10, batching: true })

// Run something with a timeout
Effect.timeout(eff, "5 seconds")           // fails with TimeoutException
Effect.timeoutOption(eff, "5 seconds")     // returns Option<A>

// Race against a deadline
Effect.disconnect(eff)                      // detaches from parent (rare)
```

## Interruption and cancellation

When a fiber is interrupted, the interruption flows through `.await` points and triggers all `Scope` finalizers. This is what makes resource cleanup automatic.

```ts
const guarded = Effect.gen(function* () {
  yield* Effect.acquireRelease(
    Effect.sync(() => console.log("acquired")),
    () => Effect.sync(() => console.log("released"))
  )
  yield* Effect.sleep("10 seconds")
})

// Even if interrupted at 1s, "released" still prints
Effect.timeout(guarded, "1 second")
```

Critical sections must disable interruption:

```ts
Effect.uninterruptible(criticalWork)        // can't be interrupted
Effect.uninterruptibleMask((restore) =>
  Effect.gen(function* () {
    yield* setupWithoutCancellation
    yield* restore(mainWork)                 // interruptible inside
    yield* teardownWithoutCancellation
  })
)
```

## Supervision

Forks attach to the enclosing fiber by default. Common variants:

```ts
Effect.fork(eff)            // child of current fiber
Effect.forkDaemon(eff)      // child of root — survives parent (use sparingly)
Effect.forkScoped(eff)      // tied to a Scope, lives until scope closes
Effect.forkIn(scope)(eff)   // tied to a specific Scope
```

`forkDaemon` is for genuinely background work (metrics flush, log shipping). Default to scoped/structured forks.

## Common pitfalls

- **Forgetting to `Fiber.join`** — orphaned fibers get interrupted when the parent ends. Sometimes that's what you want; sometimes you've lost data.
- **`forkDaemon` everywhere** — defeats structured concurrency. Use only for genuinely independent background tasks.
- **Holding non-Effect locks across `.await`** — same as Tokio's mutex problem. Use Effect's `Semaphore` or build state into the layer.
- **Assuming Promises and fibers compose** — wrapping a Promise via `Effect.tryPromise` doesn't make the underlying Promise cancellable. Real cancellation needs an `AbortSignal`-aware producer (e.g. `fetch(url, { signal })`).

## See also

- [resource-management](resource-management.md) — `Scope` ties resources to fibers
- [schedule-and-retry](schedule-and-retry.md) — `Effect.timeout` and retry
- [data-types](data-types.md) — `Deferred`, `Queue`, `Semaphore`
