# Streams

## Contents
- `Stream<A, E, R>` vs `Effect<A, E, R>`
- Constructors
- Transformations
- Sinks
- Channels (low-level)
- When to choose Stream

## `Stream<A, E, R>` vs `Effect<A, E, R>`

A **Stream** produces zero-or-more values over time, with the same `E` and `R` channels. An **Effect** produces exactly one value (or fails). Streams are pull-based and **back-pressured**: downstream determines pace.

Use Stream when:
- Items arrive over time (events, queue messages, lines from a file)
- The data set is too big to materialize (DB cursors, large files)
- You want pipelined transformations (parse → enrich → write)
- You need rate-limiting/back-pressure naturally

Use Effect when:
- A single result (even a `Chunk<A>` collected from a stream is fine)
- One-shot operations

## Constructors

```ts
import { Stream, Effect, Chunk } from "effect"

Stream.make(1, 2, 3)
Stream.fromIterable([1, 2, 3])
Stream.fromEffect(getNextBatch)            // single value from an Effect
Stream.fromIterableEffect(loadAllRows)
Stream.iterate(0, (n) => n + 1)            // 0, 1, 2, ...
Stream.repeatEffect(fetchOne)               // unbounded poll
Stream.async<number>((emit) => {            // adapter from callback APIs
  ws.on("message", (m) => emit.single(m))
  ws.on("close", () => emit.end)
})

// From an HTTP response (in @effect/platform/HttpClient)
HttpClient.get(url).pipe(
  Effect.flatMap((resp) => resp.stream)     // Stream of bytes
)
```

## Transformations

```ts
Stream.map(s, fn)
Stream.mapEffect(s, fn)                     // map with Effect side-effects
Stream.filter(s, pred)
Stream.flatMap(s, (a) => innerStream)
Stream.take(s, n)
Stream.drop(s, n)
Stream.takeWhile(s, pred)
Stream.scan(s, init, fn)                    // running fold
Stream.tap(s, fn)                           // observe each element
Stream.grouped(s, n)                        // chunks of n
Stream.throttle(s, options)                 // rate limit
Stream.debounce(s, "100 millis")
Stream.mapEffect(s, fn, { concurrency: 10 }) // parallel processing
```

## Sinks

A `Sink<A, In, L, E, R>` consumes a Stream and produces a result. Common sinks:

```ts
Sink.collectAll<A>()                  // → Chunk<A>
Sink.head<A>()                         // → Option<A>
Sink.last<A>()                         // → Option<A>
Sink.count                             // → number
Sink.sum                               // → number
Sink.fold(init, fn)                    // → accumulated value
Sink.forEach(fn)                       // → void; runs Effect for each item
```

```ts
const result = yield* Stream.run(
  Stream.fromIterable([1, 2, 3]),
  Sink.fold(0, (acc, x) => acc + x)
)
// result: 6

const all = yield* Stream.runCollect(Stream.make(1, 2, 3))
// all: Chunk<number>
```

## Channels (low-level)

`Channel` is what `Stream` and `Sink` are built from — a bidirectional, decoupled pipe with input, output, error, done, and environment channels. Use only when you need custom protocols or batching schemes the high-level API doesn't cover.

## When to choose Stream

| Need | Stream? |
|---|---|
| Process a 10GB file line by line | Yes |
| Tail a log file with backoff | Yes |
| Fan out a queue to N workers with concurrency | Yes |
| Read 5 records from a DB and return | No — use `Effect.all` |
| Single fetch and parse | No |
| WebSocket message pipeline | Yes |

Streams compose with Effect — `Stream.fromEffect`, `Stream.runForEach(fn)` returns `Effect<void, E, R>`. They're not a separate world.

## See also

- [fibers-and-concurrency](fibers-and-concurrency.md) — Stream uses fibers internally
- [data-types](data-types.md) — `Chunk`, `Queue`, `PubSub` for stream backings
- [resource-management](resource-management.md) — Stream resources need scopes
