# Runtime and Execution

## Contents
- The three runners
- `Exit` and `Cause`
- Where to run effects
- Custom runtimes
- Common pitfalls

## The three runners

| Runner | Returns | Use when |
|---|---|---|
| `Effect.runPromise(eff)` | `Promise<A>` | Async edge — HTTP handler, CLI, async test |
| `Effect.runPromiseExit(eff)` | `Promise<Exit<A, E>>` | You want to inspect failures without rejection |
| `Effect.runSync(eff)` | `A` | Synchronous edge — pure script, sync test (throws on async) |
| `Effect.runSyncExit(eff)` | `Exit<A, E>` | Same as above, no throw |
| `Effect.runFork(eff)` | `RuntimeFiber<A, E>` | Fire and forget; you'll observe later |

`runPromise` rejects with the *defect cause* (or a typed `E` wrapped in a `FiberFailure`). It does not give you the structured `Exit` — use `runPromiseExit` if you care about the difference between failure and defect.

`runSync` will *throw* if the effect contains anything async (e.g. a `Promise` constructor) — use it only for genuinely synchronous programs.

## `Exit` and `Cause`

`Exit<A, E>` is a discriminated union:

```ts
type Exit<A, E> =
  | { _tag: "Success", value: A }
  | { _tag: "Failure", cause: Cause<E> }
```

`Cause<E>` is a tree, not just a single error — it captures:
- `Fail(e)` — typed failure
- `Die(unknown)` — defect (bug)
- `Interrupt(fiberId)` — cancellation
- `Sequential(left, right)` / `Parallel(left, right)` — composed causes (e.g. when multiple parallel fibers fail)

Inspect with `Cause.failures(cause)`, `Cause.defects(cause)`, `Cause.pretty(cause)`.

## Where to run effects

> Push `runPromise` to the very edge — HTTP handler, CLI main, scheduled job entry. Never inside business logic.

Anti-pattern:
```ts
function getUser(id: string): Promise<User> {
  return Effect.runPromise(getUserEffect(id))   // ❌ defeats the type system
}
```

Pattern:
```ts
// business logic stays Effect-typed
const getUserEffect = (id: string) => /* ... */

// only the framework-edge crosses out
app.get("/users/:id", async (req, res) => {
  const exit = await Effect.runPromiseExit(
    getUserEffect(req.params.id).pipe(Effect.provide(AppLive))
  )
  if (exit._tag === "Success") res.json(exit.value)
  else res.status(500).json(Cause.pretty(exit.cause))
})
```

## Custom runtimes

For app servers, build a runtime once and reuse it:

```ts
import { ManagedRuntime } from "effect"

const runtime = ManagedRuntime.make(AppLive)
// reuse across requests:
runtime.runPromise(myEffect)
// at shutdown:
await runtime.dispose()
```

Benefits:
- Layers are built once (DB connections, OTel tracer, etc. — not per request)
- Finalizers run when `dispose` is called (graceful shutdown)

## Common pitfalls

- **Calling `runPromise` per request without a `ManagedRuntime`** — rebuilds your entire layer graph (DB pools, tracers) on every call.
- **Using `runSync` on an async effect** — throws `AsyncFiberException`. If unsure, use `runPromise`.
- **Forgetting to provide all services** — TypeScript will tell you (`R` channel must be `never`). Don't suppress with `as any`.
- **`runPromise` vs `runPromiseExit`** — `runPromise` rejects with a wrapped `FiberFailure`; expected errors look like crashes in logs. Prefer `runPromiseExit` at the edge so you can route failures vs defects deliberately.

## See also

- [services-and-layers](services-and-layers.md) — building the `AppLive` layer
- [error-handling](error-handling.md) — failure vs defect distinction
- [observability](observability.md) — `Cause.pretty` for logs
