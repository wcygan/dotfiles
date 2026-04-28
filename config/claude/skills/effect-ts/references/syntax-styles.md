# Syntax Styles: Generators vs Pipes

## Contents
- The two styles
- When to use generators
- When to use pipes
- Mixing styles
- Performance myth

## The two styles

Effect ships two equally-supported APIs:

**Generator style** — `Effect.gen` + `yield*`. Reads top-to-bottom like async/await.

```ts
const program = Effect.gen(function* () {
  const user = yield* getUser(id)
  const orders = yield* getOrders(user.id)
  return orders.length
})
```

**Pipe style** — `pipe(value, ...fns)` or `eff.pipe(Effect.flatMap, …)`. Reads as a transformation chain.

```ts
const program = pipe(
  getUser(id),
  Effect.flatMap((user) => getOrders(user.id)),
  Effect.map((orders) => orders.length)
)
```

Both compile to the same internal representation. Effect's docs are explicit:

> "If you don't have a problem with async-await you won't have a problem with Effect's generators." — [Myths](https://effect.website/docs/additional-resources/myths/)

## When to use generators

- Sequential business logic with multiple `yield*` points
- Code that reads naturally as imperative steps
- Need access to multiple intermediate values
- Onboarding mostly-async/await teams

```ts
Effect.gen(function* () {
  const config = yield* Config
  const db = yield* Database
  const user = yield* db.findUser(config.adminId)
  yield* logger.info(`admin: ${user.email}`)
  return user
})
```

## When to use pipes

- Single transformation (one or two steps)
- Building reusable combinators
- When you want point-free style or `pipe` composition with non-Effect code (`Array.map`, `Option.map`)

```ts
const upperEmail = (u: User) => pipe(
  Effect.succeed(u.email),
  Effect.map((s) => s.toUpperCase())
)
```

## Mixing styles

Free to mix. A common idiom is generator-style for the outer flow and pipe-style for tactical operators:

```ts
Effect.gen(function* () {
  const result = yield* fetchUser(id).pipe(
    Effect.timeout("3 seconds"),
    Effect.retry(retryPolicy)
  )
  return result
})
```

`yield*` accepts:
- An `Effect`
- A `Context.Tag` (yielding gives you the service)
- Any object with `[Symbol.iterator]` returning Effects (Option/Either are iterable)

## Performance myth

The "generators are slow" claim is outdated. V8 optimizes generators well, and Effect's runtime is the same machinery either way. The official docs spell out: pick whichever your team prefers.

What *is* true:
- Stack traces in generators sometimes land in runtime internals
- Step-debugging through `Effect.gen` can be noisy
- Use `Cause.pretty` for human-readable errors instead of relying on raw stack traces

## See also

- [the-effect-type](the-effect-type.md) — what `yield*` actually does
- [best-practices](best-practices.md) — idiomatic recommendations
