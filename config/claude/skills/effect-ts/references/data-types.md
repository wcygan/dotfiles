# Data Types

## Contents
- `Option` and `Either`
- `Chunk`
- Concurrent primitives: `Ref`, `Deferred`, `Queue`, `PubSub`, `Semaphore`
- Other: `Duration`, `DateTime`, `Redacted`, `BigDecimal`

## `Option` and `Either`

`Option<A>` — `Some(a)` or `None`. For "value may be missing."

```ts
import { Option } from "effect"

Option.some(42)
Option.none()
Option.fromNullable(maybe)
Option.match(opt, { onSome: (x) => …, onNone: () => … })
Option.getOrElse(opt, () => fallback)
Option.map(opt, (x) => x + 1)
Option.flatMap(opt, (x) => Option.fromNullable(x.parent))
```

`Either<R, L>` (note the order: right is success). For "two possible types."

```ts
import { Either } from "effect"

Either.right(42)
Either.left("error")
Either.match(e, { onRight: …, onLeft: … })
Either.getOrElse(e, (l) => …)
```

Both are *iterable* — you can `yield* opt` inside `Effect.gen` to short-circuit on `None` / `Left`.

## `Chunk`

`Chunk<A>` is an immutable sequence with O(1) append and prepend, optimized for stream processing:

```ts
import { Chunk } from "effect"

Chunk.empty<number>()
Chunk.make(1, 2, 3)
Chunk.fromIterable(arr)
Chunk.append(c, x)
Chunk.prepend(c, x)
Chunk.concat(a, b)
Chunk.size(c)
Chunk.toReadonlyArray(c)
```

Stream operations produce Chunks; convert to plain arrays at the boundary.

## Concurrent primitives

### `Ref<A>` — atomic mutable cell

```ts
import { Ref, Effect } from "effect"

const program = Effect.gen(function* () {
  const ref = yield* Ref.make(0)
  yield* Ref.update(ref, (n) => n + 1)
  const v = yield* Ref.get(ref)
  return v
})
```

For state that needs *async* updates: `SynchronizedRef`.

### `Deferred<A, E>` — single-shot promise

```ts
const d = yield* Deferred.make<string, never>()
yield* Effect.fork(Deferred.succeed(d, "hi").pipe(Effect.delay("1 second")))
const v = yield* Deferred.await(d)
```

### `Queue<A>` — bounded FIFO

```ts
const q = yield* Queue.bounded<number>(100)
yield* Queue.offer(q, 42)
const x = yield* Queue.take(q)
```

Variants: `unbounded`, `dropping`, `sliding` (back-pressure strategies).

### `PubSub<A>` — fan-out broadcast

```ts
const hub = yield* PubSub.bounded<Event>(64)
const subscriber = yield* PubSub.subscribe(hub)   // scoped Queue
yield* PubSub.publish(hub, event)
```

### `Semaphore` — bounded concurrency

```ts
const sem = yield* Effect.makeSemaphore(10)
yield* sem.withPermits(1)(work)
```

## Other useful types

```ts
Duration.seconds(5)
Duration.millis(100)
Duration.hours(2)
// pass durations as strings too: "5 seconds", "100 millis"

DateTime.now                                 // Effect<DateTime, never, never>
DateTime.unsafeMake(/* ... */)

Redacted.make("secret")                       // prints as "<redacted>"
// extract only via Redacted.value(r) at point of use

BigDecimal.fromString("0.1").pipe(
  BigDecimal.sum(BigDecimal.fromString("0.2"))
)  // exact arithmetic
```

## See also

- [error-handling](error-handling.md) — `Either`/`Option` interop with effects
- [fibers-and-concurrency](fibers-and-concurrency.md) — `Queue`/`PubSub`/`Semaphore` for coordination
- [streams](streams.md) — `Chunk` is the stream backing
