# Schedule and Retry

## Contents
- The `Schedule` abstraction
- Built-in schedules
- Composing schedules
- `retry` vs `repeat`
- Timeouts
- Cron and rate limiting

## The `Schedule` abstraction

A `Schedule<Out, In, R>` describes "when to do something next." It's input-aware and composable. The same schedule drives `Effect.retry`, `Effect.repeat`, periodic jobs, and rate limiters.

The shape is roughly: given an input value (or error) and elapsed time, produce a delay before the next attempt and an output value.

## Built-in schedules

```ts
import { Schedule } from "effect"

// Time-based
Schedule.spaced("100 millis")            // fixed delay between attempts
Schedule.fixed("1 second")               // fixed wall-clock interval (skips delays if work runs over)
Schedule.exponential("100 millis")       // 100, 200, 400, 800, …
Schedule.exponential("100 millis", 1.5)  // factor 1.5

// Count-based
Schedule.recurs(5)                        // run up to 5 times
Schedule.once                             // run exactly once
Schedule.forever                          // never stops

// Conditional
Schedule.recurWhile((x) => x < 10)
Schedule.recurUntil((x) => x === target)
```

## Composing schedules

```ts
// Both must allow continuation: AND semantics
Schedule.intersect(Schedule.exponential("100 millis"), Schedule.recurs(5))

// Either allows continuation: OR semantics
Schedule.union(scheduleA, scheduleB)

// Add jitter (anti-thundering-herd)
Schedule.jittered(Schedule.exponential("100 millis"))

// Cap delay at a maximum
Schedule.exponential("100 millis").pipe(Schedule.upTo("10 seconds"))
```

A robust HTTP retry policy:

```ts
const httpRetryPolicy = Schedule.exponential("100 millis").pipe(
  Schedule.intersect(Schedule.recurs(5)),
  Schedule.jittered
)
```

## `retry` vs `repeat`

- **`Effect.retry(eff, schedule)`** — retries on **failure**, until the schedule says stop or the effect succeeds.
- **`Effect.repeat(eff, schedule)`** — repeats on **success**, useful for polling.

```ts
const robustFetch = fetchUser(id).pipe(
  Effect.retry(httpRetryPolicy)
)

const poll = checkStatus.pipe(
  Effect.repeat(Schedule.spaced("5 seconds").pipe(Schedule.recurs(60)))
)
```

Variants: `retryN(eff, n)`, `retryOrElse`, `retryUntil`, `repeatN`.

## Timeouts

```ts
Effect.timeout(eff, "5 seconds")
// fails with TimeoutException after 5s; interrupts the underlying fiber

Effect.timeoutFail(eff, { duration: "5 seconds", onTimeout: () => new MyTimeout() })

Effect.timeoutOption(eff, "5 seconds")
// returns Option<A> — None on timeout, Some on success
```

`timeout` triggers structured cancellation — finalizers in the underlying effect run.

## Cron and rate limiting

```ts
import { Schedule, Effect, Cron } from "effect"

// Cron: run every Monday at 09:00
const cron = Cron.parse("0 9 * * MON").pipe(
  Effect.flatMap((c) => Effect.repeat(myJob, Schedule.cron(c)))
)

// Rate limit: at most 100 ops per second
const limiter = Effect.gen(function* () {
  const limit = yield* RateLimiter.make({ limit: 100, interval: "1 second" })
  return limit
})
```

## See also

- [error-handling](error-handling.md) — typed errors as the input to retry
- [fibers-and-concurrency](fibers-and-concurrency.md) — `timeout` cancellation semantics
- [observability](observability.md) — instrument retries with metrics
