# Error Handling

## Contents
- The two channels: failure vs defect
- Tagged errors with `Data.TaggedError`
- Recovery operators
- Wrapping thrown errors
- `Either` and `Option` interop

## The two channels

Effect splits errors into two distinct channels:

| Channel | Type | Recoverable? | When |
|---|---|---|---|
| **Failure** | typed `E` | Yes | Domain/expected errors — must be in signature |
| **Defect** | `unknown` (via `Cause.Die`) | Only via `catchAllCause` | Bugs, never-supposed-to-happen |

> Treat *failure* as "the user can do something about it" (e.g. invalid input, rate limited, declined card) and *defect* as "we have a bug" (null pointer, missing required env var at startup, unreachable code).

`Effect.fail(e)` puts `e` in the failure channel. `Effect.die(reason)` puts it in the defect channel and bypasses `E`. `throw` inside `Effect.sync` is captured as a defect.

## Tagged errors with `Data.TaggedError`

The idiom:

```ts
import { Data } from "effect"

class UserNotFound extends Data.TaggedError("UserNotFound")<{
  readonly id: string
}> {}

class RateLimited extends Data.TaggedError("RateLimited")<{
  readonly retryAfterMs: number
}> {}
```

Each instance has `_tag` set to the literal string. That powers exhaustive narrowing:

```ts
program.pipe(
  Effect.catchTag("UserNotFound", (e) => Effect.succeed(`No user ${e.id}`)),
  Effect.catchTag("RateLimited", (e) => Effect.sleep(`${e.retryAfterMs} millis`).pipe(Effect.zipRight(program)))
)
```

After each `catchTag`, the corresponding tag is **removed from the `E` channel** in the type — TypeScript tracks recovery.

For one-shot errors that don't need extra fields, use `Data.Error` or just a class extending `Data.TaggedError`.

## Recovery operators

| Operator | Behavior |
|---|---|
| `Effect.catchTag("Tag", fn)` | Recover one tag; type-narrows |
| `Effect.catchTags({ TagA: fnA, TagB: fnB })` | Multiple tags at once |
| `Effect.catchAll(fn)` | Recover any failure (collapses `E` to `never` if total) |
| `Effect.catchAllCause(fn)` | Recover failures **and defects** — last resort |
| `Effect.orElse(() => alternative)` | Discard error, run alternative |
| `Effect.orElseSucceed(() => fallback)` | Discard error, return fallback value |
| `Effect.either(eff)` | `Effect<Either<E,A>, never, R>` — moves E into success channel |
| `Effect.option(eff)` | `Effect<Option<A>, never, R>` — discards error |
| `Effect.mapError(fn)` | Transform `E` without recovering |
| `Effect.tapError(fn)` | Side effect on failure (logging) |

## Wrapping thrown errors

For sync code that throws:

```ts
const parsed = Effect.try({
  try: () => JSON.parse(input),
  catch: (cause) => new ParseError({ cause })
})
// parsed: Effect<unknown, ParseError, never>
```

For Promises:

```ts
const fetched = Effect.tryPromise({
  try: () => fetch(url).then((r) => r.json()),
  catch: (cause) => new NetworkError({ cause })
})
```

Without the `catch` mapping, `Effect.try` produces an `UnknownException` and `Effect.promise` lets rejections become defects — usually you want explicit error types.

## `Either` and `Option` interop

```ts
import { Either, Option } from "effect"

// Inside Effect.gen, you can yield Either / Option directly:
Effect.gen(function* () {
  const parsed: number = yield* Either.right(42)        // success
  const v: number = yield* Option.some(7)               // success
  const fail: never = yield* Option.none()              // fails with NoSuchElementException
})
```

Use `Either.fromNullable`, `Option.fromNullable`, `Effect.fromEither`, `Effect.fromOption` to convert at the boundaries.

## See also

- [the-effect-type](the-effect-type.md) — what fits in `E`
- [runtime-and-execution](runtime-and-execution.md) — how `Cause` surfaces failures vs defects
- [data-types](data-types.md) — Either, Option in depth
