# Schema (Validation, Encode/Decode)

## Contents
- `Schema<Type, Encoded, Requirements>`
- Defining schemas
- Decode and encode
- Branded types and refinements
- Transformations
- Generators (Arbitrary, JSON Schema, Equivalence)

## `Schema<Type, Encoded, Requirements>`

A schema is a *bidirectional* transformation. Unlike Zod (parser only), Effect Schema:

- **Decodes** from `Encoded` (e.g. JSON value, FormData) → `Type` (your domain model)
- **Encodes** the other way (`Type` → `Encoded`)
- Can require services in `Requirements` if a transformation needs them

```ts
import { Schema } from "effect"

const User = Schema.Struct({
  id: Schema.String,
  email: Schema.String,
  age: Schema.Number,
  createdAt: Schema.Date,        // decodes from string, encodes back to string
})
// User: Schema<{ id: string; email: string; age: number; createdAt: Date },
//              { id: string; email: string; age: number; createdAt: string }>
```

The `Encoded` form is what JSON.parse gives you; `Type` is what your code uses.

## Defining schemas

```ts
Schema.String                              // string
Schema.Number                              // number
Schema.Boolean                             // boolean
Schema.Date                                // Date (string ↔ Date)
Schema.NullOr(Schema.String)               // string | null
Schema.UndefinedOr(Schema.String)          // string | undefined
Schema.Array(User)                         // User[]
Schema.Record({ key: Schema.String, value: Schema.Number })
Schema.Tuple(Schema.String, Schema.Number)
Schema.Union(Schema.String, Schema.Number)
Schema.Literal("admin", "user")
Schema.optional(Schema.String)             // partial field

// With defaults
Schema.optionalWith(Schema.String, { default: () => "anon" })

// Nominal types via TaggedStruct (gets a `_tag` field)
Schema.TaggedStruct("Cat", { name: Schema.String })
```

Filters and refinements:

```ts
const Email = Schema.String.pipe(
  Schema.filter((s) => s.includes("@") || "must contain @"),
  Schema.brand("Email")
)
type Email = typeof Email.Type   // string & Brand<"Email">
```

## Decode and encode

```ts
const decoder = Schema.decodeUnknown(User)        // Effect<User, ParseError, never>
const encoder = Schema.encode(User)               // Effect<Encoded, ParseError, never>

const program = Effect.gen(function* () {
  const json = JSON.parse(input)
  const user = yield* decoder(json)               // typed parse errors
  // ...
  const back = yield* encoder(user)               // round-trip
})
```

Variants:
- `decodeUnknown` — input is `unknown` (typical from JSON, fetch)
- `decode` — input matches `Encoded` (typical for in-process boundaries)
- `validate` — input is already typed; just check refinements
- `*Sync`, `*Either`, `*Promise`, `*Effect` — choose your runner

## Branded types and refinements

```ts
const UserId = Schema.String.pipe(Schema.brand("UserId"))
type UserId = typeof UserId.Type     // string & Brand<"UserId">

function loadUser(id: UserId): Effect.Effect<User, …> { /* ... */ }
loadUser("abc")             // ❌ type error
loadUser(decoded.id as UserId)  // ✓
```

Brands cost nothing at runtime but force callers to go through validation.

## Transformations

The most powerful feature — encode/decode pairs:

```ts
const Trimmed = Schema.transform(
  Schema.String,                    // from
  Schema.String,                    // to
  { strict: true,
    decode: (s) => s.trim(),
    encode: (s) => s }              // identity on encode
)

const NumberFromString = Schema.NumberFromString
// already built-in: parses numeric strings, fails on garbage
```

Composable: `Schema.transform(input, output, { decode, encode })` where decode and encode are themselves Effects allow reading from services (e.g. lookup-by-id transforms).

## Generators

Schema doubles as a description from which other artifacts are derived:

```ts
import { Arbitrary, FastCheck, JSONSchema, Equivalence } from "effect"

// Property-based testing data
const arb = Arbitrary.make(User)            // FastCheck.Arbitrary<User>
FastCheck.assert(FastCheck.property(arb, (u) => /* invariant */))

// JSON Schema (e.g. for OpenAPI)
const json = JSONSchema.make(User)

// Structural equivalence
const eq = Equivalence.make(User)
eq(a, b)
```

This is the part Zod doesn't match: one source of truth → parser, JSON schema, fake data, equality.

## See also

- [error-handling](error-handling.md) — `ParseError` is a typed failure
- [data-types](data-types.md) — `Brand`, `Option`, `Either` interop
- [gotchas-and-tradeoffs](gotchas-and-tradeoffs.md) — Schema vs Zod tradeoffs
