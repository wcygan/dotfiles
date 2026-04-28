# Services and Layers (DI)

## Contents
- Service definition with `Context.Tag`
- Building Layers
- Composition: `mergeAll` vs `provide`
- Scoped layers (resources)
- Test doubles
- The `Config` module

## Service definition

A service is a typed contract identified by a `Context.Tag`:

```ts
import { Context, Effect } from "effect"

class Database extends Context.Tag("@app/Database")<
  Database,
  {
    readonly query: <T>(sql: string) => Effect.Effect<T[], DbError>
    readonly tx: <A, E, R>(eff: Effect.Effect<A, E, R>) => Effect.Effect<A, E | DbError, R>
  }
>() {}
```

The first type arg is the *identifier type* (the class itself); the second is the *shape* of the service. The string tag must be unique across the app — convention is `"@scope/Name"`.

Use it inside an effect by yielding the tag:

```ts
const findUser = (id: string) => Effect.gen(function* () {
  const db = yield* Database  // typed as the shape above
  return yield* db.query<User>(`select * from users where id = $1`)
})
// findUser: Effect<User[], DbError, Database>
```

The `Database` requirement now appears in `R`.

## Building Layers

A `Layer<RIn, E, ROut>` is a recipe for constructing services. Common constructors:

```ts
import { Layer } from "effect"

// Constant value
const DatabaseTest = Layer.succeed(Database, Database.of({
  query: () => Effect.succeed([]),
  tx: (e) => e,
}))

// Effect-based construction (uses other services)
const DatabaseLive = Layer.effect(
  Database,
  Effect.gen(function* () {
    const config = yield* Config
    const pool = yield* Effect.tryPromise(() => createPool(config.dbUrl))
    return Database.of({
      query: (sql) => Effect.tryPromise(() => pool.query(sql)),
      tx: (e) => /* ... */,
    })
  })
)

// Scoped (with finalizer — see resource-management.md)
const DatabaseScoped = Layer.scoped(
  Database,
  Effect.acquireRelease(
    Effect.tryPromise(() => createPool(...)),
    (pool) => Effect.promise(() => pool.end())
  ).pipe(Effect.map((pool) => Database.of({ query: ..., tx: ... })))
)
```

## Composition

Two combinators do the heavy lifting:

```ts
Layer.merge(a, b)            // both layers in parallel; combined ROut
Layer.mergeAll(a, b, c, ...)  // n-ary merge

Layer.provide(outer, inner)   // inner provides outer's RIn
// Result: outer's ROut, with inner's RIn becoming the combined RIn
```

Typical app-level composition:

```ts
const ConfigLive = Layer.succeed(Config, /* ... */)
const LoggerLive = Layer.effect(Logger, /* uses Config */).pipe(Layer.provide(ConfigLive))
const DatabaseLive = Layer.effect(Database, /* uses Config, Logger */)
  .pipe(Layer.provide(Layer.mergeAll(ConfigLive, LoggerLive)))

const AppLive = Layer.mergeAll(ConfigLive, LoggerLive, DatabaseLive)
//   ^ all services available; RIn = never
```

Then at the edge: `program.pipe(Effect.provide(AppLive))`.

## Test doubles

Swap a single layer for a test version. No mocking framework needed:

```ts
const TestDatabase = Layer.succeed(Database, Database.of({
  query: <T>() => Effect.succeed([] as T[]),
  tx: (e) => e,
}))

const TestApp = Layer.mergeAll(ConfigLive, LoggerLive, TestDatabase)

await Effect.runPromise(myProgram.pipe(Effect.provide(TestApp)))
```

Layers are referentially transparent — `TestDatabase` is just data describing how to build the service.

## The `Config` module

Effect ships first-class config reading with typed errors:

```ts
import { Config, Effect } from "effect"

const dbUrl = Config.string("DATABASE_URL")
const port = Config.integer("PORT").pipe(Config.withDefault(3000))
const settings = Config.all({ dbUrl, port })

const program = Effect.gen(function* () {
  const { dbUrl, port } = yield* settings
  // ...
})
// fails with ConfigError if env var is missing/invalid
```

`Config.redacted` produces a `Redacted<string>` that prints as `<redacted>` to prevent accidental logging of secrets.

## See also

- [the-effect-type](the-effect-type.md) — what `R` represents
- [resource-management](resource-management.md) — `Layer.scoped` for resources
- [best-practices](best-practices.md) — layer composition idioms
