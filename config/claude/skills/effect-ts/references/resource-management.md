# Resource Management

## Contents
- The `Scope` model
- `acquireRelease` and `addFinalizer`
- `Effect.scoped` — running scoped effects
- Layer scoping
- Patterns: connection pools, file handles

## The `Scope` model

A `Scope` is a *value* representing a region in which finalizers will run. Anything that takes resources — DB connections, file handles, child fibers — registers a finalizer with the active scope. When the scope closes (success, failure, or interrupt), all finalizers run in reverse order.

This replaces `try { ... } finally { ... }` with something *composable*. You don't have to remember to release; the scope does.

## `acquireRelease` and `addFinalizer`

```ts
import { Effect } from "effect"

const handle = Effect.acquireRelease(
  // acquire
  Effect.tryPromise({
    try: () => fs.promises.open("./data", "r"),
    catch: (e) => new IOError({ cause: e }),
  }),
  // release — receives the acquired value
  (file) => Effect.promise(() => file.close())
)
// handle: Effect<FileHandle, IOError, Scope>
```

The `Scope` requirement appears in `R`. The effect is now "needs a scope to run in." That requirement gets discharged by `Effect.scoped`.

For one-off finalizers without a paired acquire:

```ts
yield* Effect.addFinalizer((exit) => Effect.sync(() =>
  console.log(exit._tag === "Success" ? "ok" : "failed")
))
```

## `Effect.scoped` — running scoped effects

Wrap any scoped effect to discharge the `Scope`:

```ts
const program = Effect.scoped(
  Effect.gen(function* () {
    const file = yield* handle           // resource acquired
    const data = yield* readAll(file)    // use it
    return data
    // file automatically closed here, even on error/interrupt
  })
)
// program: Effect<Buffer, IOError, never>
```

`Effect.scoped` is the equivalent of `with` in Python or RAII in C++ — except composable across layers and cancellation-safe.

## Layer scoping

Most resources belong in a `Layer.scoped` so the entire app shares one acquisition:

```ts
import { Layer, Effect } from "effect"

const PostgresLive = Layer.scoped(
  Database,
  Effect.gen(function* () {
    const cfg = yield* Config
    const pool = yield* Effect.acquireRelease(
      Effect.tryPromise(() => createPool(cfg.url)),
      (p) => Effect.promise(() => p.end())
    )
    return Database.of({ query: (sql) => Effect.tryPromise(() => pool.query(sql)) })
  })
)
```

When the runtime is built (via `ManagedRuntime` or top-level `Effect.scoped`), the pool is acquired. When the runtime is disposed, the pool is closed.

## Patterns

**Sequential acquisition** — finalizers stack reverse:

```ts
Effect.gen(function* () {
  const a = yield* acquireA  // released last
  const b = yield* acquireB  // released after c
  const c = yield* acquireC  // released first
})
```

**Parallel safe acquisition** — all finalize even if one fails:

```ts
Effect.all([acquireA, acquireB, acquireC], { concurrency: "unbounded" })
```

**Conditional cleanup** — `addFinalizerExit` lets you branch:

```ts
yield* Effect.addFinalizerExit((exit) =>
  exit._tag === "Failure"
    ? rollback
    : commit
)
```

**Bracket pattern shorthand** — `Effect.acquireUseRelease`:

```ts
Effect.acquireUseRelease(
  acquire,
  (resource) => use(resource),     // body
  (resource) => release(resource)
)
```

## See also

- [services-and-layers](services-and-layers.md) — `Layer.scoped` for app resources
- [fibers-and-concurrency](fibers-and-concurrency.md) — interruption triggers finalizers
- [runtime-and-execution](runtime-and-execution.md) — `ManagedRuntime` lifetime
