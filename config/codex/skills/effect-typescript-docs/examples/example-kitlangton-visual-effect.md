# kitlangton/visual-effect Effect Examples

Snapshot: `c5ae620bb57b7f9452424dbd46c7751c9bee9490` on the `main` branch, inspected 2026-06-04.

Use these examples for visual, pedagogical Effect runtime patterns: fibers, interruption, services, resource finalizers, retry schedules, refs, validation, and outcome states.

## High-Level Read

Visual Effect is a teaching tool, so its value is different from a production backend. It turns Effect runtime concepts into UI state: running, completed, failed, interrupted, and defect/death. That makes it a compact repo for understanding how fibers, interruption, finalizers, schedules, refs, and typed failures behave at runtime.

The project wraps a user-provided `Effect.Effect<A, E>` in a class that can run, await, interrupt, reset, and visualize it. This is useful when explaining Effect because it connects abstract APIs to visible state transitions.

## Permalinks

- [VisualEffect service context](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/VisualEffect.ts#L61-L85) - `Context.GenericTag`, service interface, and service methods returning `Effect.Effect`.
- [Wrapping an Effect in UI state](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/VisualEffect.ts#L87-L145) - stores an `Effect.Effect<A, E>`, handles terminal states, and provides a parent service to nested effects.
- [Fiber run and interruption controls](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/VisualEffect.ts#L303-L345) - `Effect.runFork`, `Fiber.await`, and explicit fiber interruption from UI controls.
- [Simulated resource acquisition](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/examples/effect-acquire-release.tsx#L14-L43) - small `Effect.gen` acquisition examples with delayed setup.
- [Scoped acquire/release walkthrough](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/examples/effect-acquire-release.tsx#L84-L158) - success, failure, defect, and finalizer behavior around `Effect.acquireRelease` and `Effect.scoped`.
- [Retry with bounded schedule](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/examples/effect-retry-recurs.tsx#L23-L71) - failing effect retried with `Schedule.intersect`, `Schedule.spaced`, and `Schedule.recurs`.
- [Retry with exponential backoff](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/examples/effect-retry-exponential.tsx#L15-L53) - `Effect.retry` with `Schedule.exponential`.
- [Repeat while schedule output matches predicate](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/examples/effect-repeat-while-output.tsx#L17-L62) - `Effect.repeat`, `Schedule.elapsed`, `Schedule.whileOutput`, and `Effect.ensuring`.
- [Concurrent Ref updates](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/examples/ref-update-and-get.tsx#L16-L85) - shared `Ref`, `Ref.updateAndGet`, and `Effect.all` with unbounded concurrency.
- [Finalizers across success, failure, defect, and interruption](https://github.com/kitlangton/visual-effect/blob/c5ae620bb57b7f9452424dbd46c7751c9bee9490/src/examples/effect-add-finalizer.tsx#L53-L139) - `Effect.addFinalizer`, `Effect.fail`, `Effect.die`, interruption, and scoped cleanup.

## Code Samples

These are distilled pattern sketches from the linked code, not verbatim excerpts.

### Wrapping An Effect In Runnable UI State

```ts
class VisualEffect<A, E = never> {
  private fiber: Fiber.RuntimeFiber<A, E> | null = null
  state: EffectState<A, E> = { type: "idle" }

  constructor(
    readonly name: string,
    private readonly source: Effect.Effect<A, E>
  ) {}

  get effect(): Effect.Effect<A, E> {
    return Effect.gen(this, function* () {
      this.state = { type: "running" }
      const result = yield* this.source
      this.state = { type: "completed", result }
      return result
    })
  }

  async run() {
    this.fiber = Effect.runFork(this.effect)
    await Effect.runPromise(Fiber.await(this.fiber))
  }
}
```

### Interrupting A Running Fiber

```ts
class VisualEffect<A, E> {
  private fiber: Fiber.RuntimeFiber<A, E> | null = null

  interrupt() {
    const fiber = this.fiber
    this.fiber = null
    this.state = { type: "interrupted" }

    if (fiber) {
      Effect.runFork(Fiber.interrupt(fiber))
    }
  }
}
```

### Resource Scope With Cleanup

```ts
const makeDatabase = Effect.acquireRelease(
  connectDatabase,
  (db) => Effect.sync(() => db.close())
)

const program = Effect.gen(function* () {
  const db = yield* makeDatabase
  yield* Effect.sleep("1 second")

  if (shouldFail) {
    return yield* Effect.fail("work failed")
  }

  return yield* doWork(db)
}).pipe(Effect.scoped)
```

### Retry And Repeat Schedules

```ts
const retryWithBackoff = task.pipe(
  Effect.retry(Schedule.exponential("700 millis"))
)

const repeatWhileWithinWindow = poll.pipe(
  Effect.repeat(
    Schedule.intersect(
      Schedule.spaced("400 millis"),
      Schedule.whileOutput(Schedule.elapsed, (elapsed) =>
        Duration.lessThan(elapsed, Duration.seconds(10))
      )
    )
  )
)
```

### Concurrent Ref Updates

```ts
const increment = (counter: Ref.Ref<number>) =>
  Ref.updateAndGet(counter, (value) => value + 1)

const concurrent = Effect.gen(function* () {
  const counter = yield* Ref.make(0)

  return yield* Effect.all(
    Array.from({ length: 5 }, () => increment(counter)),
    { concurrency: "unbounded" }
  )
})
```
