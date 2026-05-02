---
name: effect-ts
description: Effect TS (`effect` library + ecosystem) expert. Use for idiomatic patterns, Layer DI, tagged errors, fibers, Schedule retries, Schema validation, Stream, runPromise, and migrating Promise code to Effect. Keywords effect, Effect.gen, pipe, Layer, Context.Tag, Data.TaggedError, Schema, Fiber, Stream, neverthrow, fp-ts.
---

# Effect TS

Effect is one library that bundles error handling, dependency injection, retries, concurrency, streaming, scheduling, schema validation, and observability — roughly the role 10+ separate npm packages usually fill. The single most important idea is the `Effect<A, E, R>` type: every computation tracks not just its success type `A`, but also its expected error type `E` and the services `R` it requires.

## The Mental Model

```
Effect<A, E, R>
  A = success value
  E = expected (recoverable) error type — must be handled or it stays in the type
  R = required services — must be provided via Layer before runtime can execute it

Effect is a LAZY DESCRIPTION of a program. Nothing runs until you hand it to a runtime
(runPromise / runSync / runFork). Compose effects, then run once at the edge.
```

Two error channels:
- **Failures** — typed, recoverable, in `E`. Created with `Effect.fail` or `Data.TaggedError` instances.
- **Defects** — untyped, unrecoverable bugs. Surface only via `Cause` / `runPromise` rejection.

Two interchangeable styles:
- **Generator** (`Effect.gen` + `yield*`) — reads like async/await; default for sequential code.
- **Pipe** (`pipe(eff, Effect.flatMap, Effect.map)`) — better for short transforms.

## Quick Decision Trees

**Concurrency primitive:**
- Need all results, no orphans? → `Effect.all({ concurrency: N })`
- First-to-complete or shutdown signal? → `Effect.race`
- Background task with cancellation? → `Effect.fork` + `Scope`
- Bounded parallelism over a list? → `Effect.forEach(items, fn, { concurrency: N })`

**Error type:**
- Single-tag domain error? → `class Foo extends Data.TaggedError("Foo")<{ ... }> {}`
- Wrap a thrown exception? → `Effect.try` / `Effect.tryPromise` with `catch`
- Recover from a specific tag? → `Effect.catchTag("Foo", handler)`
- Recover from all errors? → `Effect.catchAll` (last resort)

**Validation / parsing:**
- Just decode JSON / form data? → `Schema.decodeUnknown(MySchema)`
- Need encode (round-trip back to wire)? → `Schema.encode`
- Branded ID type? → `Schema.String.pipe(Schema.brand("UserId"))`
- Property-based test data? → `Arbitrary.make(MySchema)`

**Service / dependency:**
- Static config? → `Config` module reads env vars with typed errors
- Stateful service? → `Context.Tag` + `Layer.effect(Tag, build)`
- Test double? → swap the `Layer` at the edge; no mock framework

## Before Going All-In, Ask:

1. Does my team have the appetite for a paradigm shift? (Effect is "almost a language" — Ethan Niser)
2. Is the surface mostly Effect-native, or am I wrapping Express/Drizzle/Sentry? (Heavy boundary friction = "the Effect tax")
3. Do I need typed errors *and* DI *and* retries *and* tracing? (If yes, Effect saves you from gluing 5 libs. If just typed errors → `neverthrow`. If just schema → `Zod`/`Valibot`.)
4. Bundle floor ~25 KB gzip — acceptable?
5. v4 is in beta — do I lock to 3.x and migrate later, or wait?

## Reference Files

Detailed guidance organized by topic. Load only what's relevant.

References: [the-effect-type](references/the-effect-type.md) — `Effect<A, E, R>` mechanics, laziness, `succeed`/`fail`/`sync`/`promise`/`try`
References: [runtime-and-execution](references/runtime-and-execution.md) — `runPromise`/`runSync`/`runFork`, `Exit`, `Cause`, where to run
References: [syntax-styles](references/syntax-styles.md) — `Effect.gen` vs `pipe`, when each shines, perf myths
References: [error-handling](references/error-handling.md) — `Data.TaggedError`, `catchTag`/`catchAll`, failures vs defects, `either`/`option`
References: [services-and-layers](references/services-and-layers.md) — `Context.Tag`, `Layer`, composition, scoping, test doubles
References: [fibers-and-concurrency](references/fibers-and-concurrency.md) — fibers, `fork`, `interrupt`, `race`/`all`, structured concurrency
References: [resource-management](references/resource-management.md) — `Scope`, `acquireRelease`, `addFinalizer`, `Effect.scoped`
References: [schedule-and-retry](references/schedule-and-retry.md) — `Schedule`, exponential/jittered, `retry`/`repeat`, timeouts, `Effect.timeout`
References: [schema](references/schema.md) — `Schema`, decode/encode, branded types, transformations, JSON Schema, Arbitrary
References: [streams](references/streams.md) — `Stream`, `Sink`, `Channel`, backpressure, when to choose Stream over Effect
References: [observability](references/observability.md) — `Logger`, `Metric`, `Effect.withSpan`, OpenTelemetry export
References: [data-types](references/data-types.md) — `Option`, `Either`, `Chunk`, `Ref`, `Deferred`, `Queue`, `PubSub`
References: [best-practices](references/best-practices.md) — idioms, layer composition, edge handling, incremental adoption
References: [gotchas-and-tradeoffs](references/gotchas-and-tradeoffs.md) — bundle size, integration friction, v4 beta, alternatives

## Complementary skills

This skill owns the Effect type system and ecosystem. Hand off when the question is about *framework wiring* rather than Effect itself:

| Signal | Hand off to |
|---|---|
| `package.json` has `@tanstack/react-start`, or user is inside a TanStack Start app | **`bun-tanstack-start` — Effect TS is its declared default for server-side business logic.** Load both skills together. See [effect-integration](../bun-tanstack-start/references/effect-integration.md) for `ManagedRuntime` placement, `runPromiseExit` inside `createServerFn`, and Schema-as-validator. |
| User asks how to wire `Layer`s into a server's request lifecycle on Bun | `bun-tanstack-start` (owns the boundary) |
| Question is about `vite.config.ts`, Nitro presets, or `__root.tsx` | `bun-tanstack-start` |

Rule of thumb: **Effect lives at the seams, not the wiring.** This skill explains the seam (`runPromiseExit` and `Cause` routing — see [runtime-and-execution](references/runtime-and-execution.md) and [error-handling](references/error-handling.md)). The framework skill explains where the seam goes.
