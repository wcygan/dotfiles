# Effect TS Integration with TanStack Start

**Effect TS is the default for server-side business logic in this stack.** This is the wiring doc that connects the framework (TanStack Start on Bun) to the type system (`effect-ts`). Load the `effect-ts` skill for the deep dives on types/Layers/Schema/Schedule/etc.

If you're scaffolding a new app and effect isn't installed, that's a setup gap — fix it:

```bash
bun add effect
# Then create src/server/runtime.ts with a ManagedRuntime as shown below.
```

Opt-out is allowed for trivial server functions (e.g. a static "/health" handler returning `{ ok: true }`) but should be marked with a `// effect-ts skipped: <reason>` comment. For anything that talks to a database, calls an external API, or has multiple failure modes, use Effect.

## The boundary rule

> Framework wiring stays in TanStack Start. Effect code lives **inside** server functions and route loaders. The conversion happens at exactly one line per call site.

What that looks like:

```
createServerFn / loader (TanStack)
        │
        │  runPromiseExit ← the boundary
        ▼
Effect<A, E, R>  (your business logic)
        │
        │  Layer.provide(AppLive)
        ▼
Database / Logger / HttpClient services
```

Two patterns avoid all the friction the [Effect Tax](../../effect-ts/references/gotchas-and-tradeoffs.md) usually causes:

1. **Build the runtime once at server boot**, not per request.
2. **Convert at the very edge** — `runPromiseExit` inside `createServerFn`/loader, never deeper.

## Build a `ManagedRuntime` once

`ManagedRuntime` materializes a `Layer` graph (DB pool, OTel tracer, etc.) so you don't rebuild it per request. Place it in a server-only module that TanStack won't ship to the client:

```ts
// src/server/runtime.ts  (server-only — keep .server.ts or use route gating)
import { ManagedRuntime, Layer } from "effect"
import { DatabaseLive } from "./layers/database"
import { LoggerLive } from "./layers/logger"
import { TracingLive } from "./layers/tracing"

const AppLive = Layer.mergeAll(DatabaseLive, LoggerLive, TracingLive)

export const runtime = ManagedRuntime.make(AppLive)
// Optional: dispose on signal for graceful shutdown
process.once("SIGTERM", () => void runtime.dispose())
```

See [services-and-layers](../../effect-ts/references/services-and-layers.md) and [runtime-and-execution](../../effect-ts/references/runtime-and-execution.md) for what goes in each Layer.

## Inside a `createServerFn`

```ts
import { createServerFn } from "@tanstack/react-start"
import { Effect, Cause } from "effect"
import { Schema } from "effect"
import { runtime } from "~/server/runtime"
import { UserNotFound, getUser } from "~/server/users"

const Input = Schema.Struct({ id: Schema.String })

export const fetchUser = createServerFn({ method: "GET" })
  .validator(Schema.decodeUnknown(Input))    // Effect Schema as the validator
  .handler(async ({ data }) => {
    const exit = await runtime.runPromiseExit(
      getUser(data.id).pipe(
        Effect.withSpan("fetchUser", { attributes: { "user.id": data.id } })
      )
    )
    if (exit._tag === "Success") return exit.value

    // route failures vs defects deliberately — see error-handling reference
    const failure = Cause.failureOption(exit.cause)
    if (failure._tag === "Some") {
      const e = failure.value
      if (e._tag === "UserNotFound") throw notFound()
      throw new Error(e._tag)               // typed but framework expects throws
    }
    console.error(Cause.pretty(exit.cause))  // it's a defect (bug)
    throw new Error("Internal error")
  })
```

Key points:
- `runPromiseExit` (not `runPromise`) so you can branch on `Cause`.
- Re-throw at the seam — TanStack/Vinxi expects thrown errors for status mapping. This is the [Effect Tax](../../effect-ts/references/gotchas-and-tradeoffs.md) talking, and it's the right place to pay it.
- `Effect.withSpan` light up traces if you wired the OTel layer ([observability](../../effect-ts/references/observability.md)).

## Inside a route loader

```ts
import { createFileRoute } from "@tanstack/react-router"
import { fetchUser } from "~/server/users.fns"

export const Route = createFileRoute("/users/$id")({
  loader: ({ params }) => fetchUser({ data: { id: params.id } }),
  component: UserPage,
})
```

The Effect-aware code stays inside `fetchUser`; the loader just calls the server function. **Do not** call `runPromise` directly in a loader — keep the boundary in one place.

## Schema as the validator

Effect Schema works as a TanStack `validator` because both `decodeUnknown` and `decode` return Effects/Promises that throw on failure:

```ts
import { Schema } from "effect"

const ChargeInput = Schema.Struct({
  amountCents: Schema.Number.pipe(Schema.int(), Schema.positive()),
  customerId: Schema.String.pipe(Schema.brand("CustomerId")),
})

export const charge = createServerFn({ method: "POST" })
  .validator(Schema.decodeUnknown(ChargeInput))
  .handler(async ({ data }) => { /* data is fully typed + branded */ })
```

See [schema](../../effect-ts/references/schema.md) for branded types, transformations, and JSON Schema generation (handy for OpenAPI on the same source).

## What stays where

| Concern | Skill |
|---|---|
| `vite.config.ts`, plugin order, `__root.tsx` stylesheet | `bun-tanstack-start` |
| `bun --bun` scripts, Nitro preset, deployment | `bun-tanstack-start` |
| `createServerFn`, route loaders, file-based routing | `bun-tanstack-start` |
| `Effect<A, E, R>`, `Layer`, `Context.Tag` | `effect-ts` |
| `Data.TaggedError`, `catchTag`, `Cause` | `effect-ts` |
| `Schema` decode/encode/branded types | `effect-ts` |
| `Schedule`, `retry`, `timeout` | `effect-ts` |
| `Stream`, fibers, `Effect.scoped` | `effect-ts` |
| Where to call `runPromiseExit`, where `ManagedRuntime` lives | **here** (this file) |

## Gotchas specific to this combination

- **Don't ship the runtime to the client.** `ManagedRuntime` references Node-only Layers (DB pool, fs). Keep it in `*.server.ts` files or behind `import.meta.env.SSR` guards. TanStack tree-shakes server-only imports from server functions; route handlers and `__root` are client-bundled.
- **`runPromise` rejection wraps in `FiberFailure`.** Use `runPromiseExit` so failure messages don't show up as opaque "FiberFailure" strings in framework error pages.
- **Vinxi error pages don't read `Cause`.** If you want pretty causes in dev, log `Cause.pretty(exit.cause)` yourself before re-throwing.
- **Bun runtime + Effect.** No known incompatibilities as of Effect 3.x — Effect runs identically on Bun and Node. The `bun --bun` flag still matters per the [non-negotiables](../SKILL.md#non-negotiables).
- **Don't `Effect.provide(AppLive)` per call.** Use `runtime.runPromiseExit` — it provides the layer once. Per-call `Effect.provide` rebuilds nothing but adds noise; reserve it for tests where you swap layers.

## See also

- [effect-ts SKILL.md](../../effect-ts/SKILL.md) — full Effect reference index
- [server-functions](server-functions.md) — TanStack `createServerFn` mechanics
- [routing](routing.md) — loader patterns
