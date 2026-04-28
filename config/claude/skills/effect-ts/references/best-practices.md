# Best Practices

## Contents
- Universal idioms
- Layer composition
- Edge handling
- Testing
- Incremental adoption strategies

## Universal idioms

These hold across teams that ship Effect successfully:

1. **Use `Effect.gen` for sequential code.** It reads like async/await and is the documented default. Reserve `pipe` for short transforms.

2. **Define errors with `Data.TaggedError`.** Gives `_tag` for `catchTag` narrowing and proper class-based equality.

3. **Build Layers bottom-up; provide once at main.** Each `Layer` declares its own dependencies; merge them into a single `AppLive` and `Effect.provide(AppLive)` only at the entry point.

4. **Don't `runPromise` inside business logic.** Push it to the very edge — HTTP handler, CLI main, scheduled job. Per-request runs through a `ManagedRuntime` so layers aren't rebuilt.

5. **Use `Effect.scoped` + `acquireRelease` for any resource.** No `try/finally`. Scopes survive cancellation and exceptions.

6. **Keep `R` as `never` at the entry point.** TypeScript will tell you what's unprovided. Don't `as any` it away.

7. **Tag every span you'd want in a flame graph.** `Effect.withSpan("name")` is cheap, propagates automatically, and lights up traces in Tempo/Honeycomb.

8. **Prefer typed failures over defects.** Defects mean "bug." If a caller might reasonably handle it, it's a failure — put it in `E`.

## Layer composition

Pattern that scales:

```ts
// One layer per service
const ConfigLive = Layer.succeed(Config, /* env-derived */)
const LoggerLive = Layer.effect(Logger, makeLogger).pipe(
  Layer.provide(ConfigLive)
)
const DatabaseLive = Layer.scoped(Database, makeDb).pipe(
  Layer.provide(Layer.mergeAll(ConfigLive, LoggerLive))
)

// Single mergeAll at the top — everything app needs
const AppLive = Layer.mergeAll(
  ConfigLive,
  LoggerLive,
  DatabaseLive,
  TracingLive,
  /* … */
)
```

Two rules:
- **A layer's `Layer.provide` should always include all of its transitive deps.** Don't rely on the consumer to know.
- **`Layer.mergeAll` is for the final composition, not intermediate layers.** Internal layers compose with `Layer.provide`.

## Edge handling

The "edge" is anywhere Effect meets non-Effect code:

```ts
// HTTP handler with Express
app.post("/charge", async (req, res) => {
  const program = chargeFlow(req.body).pipe(
    Effect.provide(AppLive),
    Effect.withSpan("POST /charge"),
    Effect.annotateLogs("requestId", req.id),
  )
  const exit = await Effect.runPromiseExit(program)
  if (exit._tag === "Success") return res.json(exit.value)
  // ⬇ KEY: route failures vs defects to different responses
  const failure = Cause.failureOption(exit.cause)
  if (Option.isSome(failure)) {
    const err = failure.value
    if (err._tag === "ValidationError") return res.status(400).json(err)
    if (err._tag === "NotFound") return res.status(404).json(err)
    return res.status(500).json({ message: "internal error" })
  }
  // it's a defect (bug) — log everything, generic 500
  log.error(Cause.pretty(exit.cause))
  res.status(500).json({ message: "internal error" })
})
```

Common edges to plan for:
- HTTP request → response
- DB transactions (the rollback is on uncaught exceptions; you may need to re-throw at the seam)
- Sentry/error monitor uploads
- Express middleware (callback-style)
- Passport auth strategies

## Testing

Use `@effect/vitest` (or `effect/Test` directly):

```ts
import { it, expect } from "@effect/vitest"
import { Effect, Layer } from "effect"

it.effect("rejects empty email", () =>
  Effect.gen(function* () {
    const result = yield* Effect.either(createUser({ email: "" }))
    expect(Either.isLeft(result)).toBe(true)
  }).pipe(Effect.provide(TestLive))
)
```

Key principles:
- Replace one layer for the test (e.g., `TestDatabase` instead of `DatabaseLive`)
- No mocking framework needed — Layers are the swap point
- `TestClock` lets you fast-forward `Schedule` and timeouts deterministically
- Property-based: combine `Schema.Arbitrary` with `fast-check`

## Incremental adoption strategies

Two camps in the community — pick deliberately:

**Surgical (Lytras's approach):**
- Use Schema for parsing at boundaries
- Use `Data.TaggedError` for tagged errors in your domain
- Skip Layer / DI; keep regular function injection
- Stay close to plain TypeScript everywhere else
- Lower onboarding cost, less paradigm shift, easier to abandon if it doesn't fit

**All-in (Effect-native):**
- HTTP server via `@effect/platform/HttpServer`
- Database via Layer with scoped pool
- All app code returns `Effect`
- One `ManagedRuntime` per app
- Higher ceiling, more leverage from the ecosystem (OTel, retries, structured concurrency for free)

**Either way, pick one boundary first** (e.g., the API request layer or one feature module) and let it stabilize before expanding.

## See also

- [services-and-layers](services-and-layers.md) — composition mechanics
- [runtime-and-execution](runtime-and-execution.md) — `ManagedRuntime` lifecycle
- [gotchas-and-tradeoffs](gotchas-and-tradeoffs.md) — known friction points
