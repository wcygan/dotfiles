# Effect TS Integration with TanStack Start

> **Opt-in.** Effect TS is a strong fit for non-trivial server logic in a TanStack Start app, but it is not required. Use it when you want typed errors, structured concurrency, retries/timeouts via `Schedule`, or a `Layer`-based DI graph. For trivial handlers (a `/health` returning `{ ok: true }`, a static lookup) plain `async`/`await` is fine.

This file is the **wiring** doc — where the seam between TanStack Start and Effect lives. For the Effect type system itself (`Effect<A, E, R>`, `Layer`, `Schema`, `Schedule`, `Data.TaggedError`), see the `effect-ts` skill.

## Table of Contents

- [The boundary rule](#the-boundary-rule)
- [Build a `ManagedRuntime` once](#build-a-managedruntime-once)
- [Inside a `createServerFn`](#inside-a-createserverfn)
- [Inside a route loader](#inside-a-route-loader)
- [Schema as the validator](#schema-as-the-validator)
- [What stays where](#what-stays-where)
- [Gotchas](#gotchas)

## The boundary rule

> Framework wiring stays in TanStack Start. Effect code lives **inside** server functions and route loaders. The conversion happens at exactly one line per call site.

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

Two patterns avoid most of the friction the [Effect Tax](../../effect-ts/references/gotchas-and-tradeoffs.md) usually causes:

1. **Build the runtime once at server boot**, not per request.
2. **Convert at the very edge** — `runPromiseExit` inside `createServerFn` / loader, never deeper.

## Setup

```bash
bun add effect    # or: npm install effect
```

Then create `src/server/runtime.ts` with a `ManagedRuntime` (next section).

## Build a `ManagedRuntime` once

`ManagedRuntime` materializes a `Layer` graph (DB pool, OTel tracer, HTTP client, etc.) so you don't rebuild it per request. Place it in a server-only module — TanStack tree-shakes server-only imports out of client bundles, but be explicit with a `*.server.ts` suffix or import-protection marker (see `import-protection.md`).

```ts
// src/server/runtime.ts (server-only)
import { ManagedRuntime, Layer } from "effect"
import { DatabaseLive } from "./layers/database"
import { LoggerLive } from "./layers/logger"
import { TracingLive } from "./layers/tracing"

const AppLive = Layer.mergeAll(DatabaseLive, LoggerLive, TracingLive)

export const runtime = ManagedRuntime.make(AppLive)

// Optional: dispose on signal for graceful shutdown
process.once("SIGTERM", () => void runtime.dispose())
```

See the `effect-ts` skill — `services-and-layers.md` and `runtime-and-execution.md` — for what goes in each Layer.

## Inside a `createServerFn`

```ts
import { createServerFn } from "@tanstack/react-start"
import { Effect, Cause, Schema } from "effect"
import { runtime } from "~/server/runtime"
import { getUser } from "~/server/users"
import { notFound } from "@tanstack/react-router"

const Input = Schema.Struct({ id: Schema.String })

export const fetchUser = createServerFn({ method: "GET" })
  .validator(Schema.decodeUnknown(Input))      // Effect Schema as the validator
  .handler(async ({ data }) => {
    const exit = await runtime.runPromiseExit(
      getUser(data.id).pipe(
        Effect.withSpan("fetchUser", { attributes: { "user.id": data.id } })
      )
    )
    if (exit._tag === "Success") return exit.value

    // Route failures vs defects deliberately — see effect-ts/error-handling.md
    const failure = Cause.failureOption(exit.cause)
    if (failure._tag === "Some") {
      const e = failure.value
      if (e._tag === "UserNotFound") throw notFound()
      throw new Error(e._tag)              // typed but framework expects throws
    }
    console.error(Cause.pretty(exit.cause)) // it's a defect (bug)
    throw new Error("Internal error")
  })
```

Key points:

- **`runPromiseExit` (not `runPromise`)** so you can branch on `Cause`. `runPromise` rejects with an opaque `FiberFailure`.
- **Re-throw at the seam.** TanStack/Vinxi expects thrown errors for HTTP status mapping. This is the right place to pay the [Effect Tax](../../effect-ts/references/gotchas-and-tradeoffs.md).
- **`Effect.withSpan`** lights up traces if you wired the OTel layer (see `effect-ts/observability.md`).

## Inside a route loader

```ts
import { createFileRoute } from "@tanstack/react-router"
import { fetchUser } from "~/server/users.fns"

export const Route = createFileRoute("/users/$id")({
  loader: ({ params }) => fetchUser({ data: { id: params.id } }),
  component: UserPage,
})
```

Effect-aware code stays inside `fetchUser`; the loader just calls the server function. **Do not** call `runPromise` directly in a loader — keep the boundary in one place.

## Schema as the validator

Effect Schema works as a TanStack `validator` because `decodeUnknown` returns a Promise that throws on failure:

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

You can use `Zod` instead — TanStack accepts any `(input) => output | Promise<output>` validator. The Schema option is offered here for projects already on Effect; the OpenAPI/JSON-Schema interop is a nice bonus.

## What stays where

| Concern | Where |
|---|---|
| `vite.config.ts`, plugin order, `__root.tsx` stylesheet | this skill (`project-setup.md`, `tailwind-and-styling.md`) |
| `createServerFn`, route loaders, file-based routing | this skill (`server-functions.md`, `routing-and-navigation.md`) |
| Nitro presets / deployment | this skill (`hosting-and-deployment.md`) |
| `Effect<A, E, R>`, `Layer`, `Context.Tag` | `effect-ts` skill |
| `Data.TaggedError`, `catchTag`, `Cause` | `effect-ts` skill |
| `Schema` decode/encode/branded types | `effect-ts` skill |
| `Schedule`, `retry`, `timeout` | `effect-ts` skill |
| `Stream`, fibers, `Effect.scoped` | `effect-ts` skill |
| Where to call `runPromiseExit`, where `ManagedRuntime` lives | **this file** |

## Gotchas

- **Don't ship the runtime to the client.** `ManagedRuntime` references Node-only Layers (DB pool, fs). Keep it in `*.server.ts` files or behind `import.meta.env.SSR` guards. See `import-protection.md`.
- **`runPromise` rejection wraps in `FiberFailure`.** Use `runPromiseExit` so failure messages don't surface as opaque "FiberFailure" strings in framework error pages.
- **TanStack error pages don't read `Cause`.** If you want pretty causes in dev, log `Cause.pretty(exit.cause)` yourself before re-throwing.
- **Bun + Effect.** No known incompatibilities — Effect runs identically on Bun and Node. The `bun --bun` flag (see the `bun` skill) still matters for the surrounding tooling.
- **Don't `Effect.provide(AppLive)` per call.** Use `runtime.runPromiseExit` — it provides the layer once. Per-call `Effect.provide` is reserved for tests where you swap layers.

## See also

- `effect-ts` skill — full Effect reference index (Layers, Schema, Cause, Schedule)
- [server-functions](server-functions.md) — `createServerFn` mechanics
- [data-loading](data-loading.md) — loader patterns
- [import-protection](import-protection.md) — keeping server code off the client
