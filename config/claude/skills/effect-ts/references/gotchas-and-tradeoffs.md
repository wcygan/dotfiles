# Gotchas and Tradeoffs

## Contents
- The Effect Tax (boundary friction)
- Bundle size
- Type-checker performance
- Stack traces and debugging
- API churn (v3 → v4)
- When NOT to use Effect
- Alternatives

## The Effect Tax

The community phrase for the friction of wrapping non-Effect libraries. Real cases practitioners hit:

**Drizzle transactions** — `db.transaction(...)` only rolls back when an *uncaught exception* propagates out. If you use `Effect.tryPromise` and surface the error as an `E`-channel value, the transaction commits. Workaround: re-throw the error inside the transaction body, or use `Effect.runPromiseExit` and re-throw on `Failure`.

**Sentry / error monitors** — most expect `process.on("uncaughtException")` semantics. With Effect, errors become typed values and the monitor never sees them. Solution: at the very edge, on `runPromiseExit` returning `Failure`, manually post the cause to Sentry with `Cause.pretty(cause)`.

**Express middleware** — `(req, res, next) => …` wants imperative control. You either wrap the whole handler in Effect (then convert at the very end) or keep middleware plain TS and only enter Effect inside route handlers.

**Passport.js** — strategies expect callback `(err, user) => …`. Wrap with `Effect.async` if you need it inside Effect; or keep auth as plain TS and convert at the boundary.

> "We'd find ourselves calling `Effect.runSync` or `Effect.runPromise` constantly… working against our own language and tech stack." — [Harbor blog](https://runharbor.com/blog/2025-11-24-why-we-dont-use-effect-ts)

The tax shrinks as more of your codebase becomes Effect-native — but it's real on day one and during incremental adoption.

## Bundle size

- Floor ~25 KB gzip even with tree-shaking ([official myths page](https://effect.website/docs/additional-resources/myths/))
- Has fluctuated up to ~10KB across versions ([issue #4484](https://github.com/Effect-TS/effect/issues/4484))
- Schema/Stream/Layer each add several KB; using all of them makes Effect the biggest dep in many bundles
- **Effect Micro** is a smaller subset shipped in the same package — use it when bundle matters
- Tree-shaking only works with proper bundler config (ESM imports, no `import * as`)

For browser-shipped code: weigh the bundle against alternatives.

## Type-checker performance

Large `Layer.mergeAll` graphs and deep `Effect.gen` blocks slow down `tsc`:

- Use `satisfies` and explicit type annotations on layers to break inference chains
- Split very large composed layers into named intermediate layers
- Watch for inference exploding when you compose many `Effect.gen` calls — sometimes a `: Effect.Effect<A, E, R>` annotation cuts seconds off compile time

If your editor's `tsserver` becomes laggy, this is usually the culprit.

## Stack traces and debugging

- Generators sometimes land in runtime internals during step-debugging
- Stack traces have improved over time but are still noisier than plain async/await
- **Use `Cause.pretty(cause)` for human-readable failure output** — much better than reading raw stacks
- `Effect.withSpan` + OTel is often a better debugging tool than stepping through code

## API churn — v3 → v4

- Effect 3.x has been stable for ~18 months
- `@effect/schema` was renamed/relocated mid-3.x — check imports if older docs disagree
- **Effect v4 is in beta** as of late 2025/early 2026 — promises smaller bundles and lower runtime overhead ([forum](https://forum.kirupa.com/t/effect-v4-beta-cuts-runtime-overhead-and-bundle-size/680627))
- v4 will require migration; track release notes before locking architecture

## When NOT to use Effect

- **Existing Express/Next.js codebase with many third-party callbacks** — friction is high
- **Team rotates frequently** — hiring market is thin and onboarding cost is real
- **You only need typed errors** — `neverthrow` or `ts-results` is far smaller
- **You only need schema validation** — `Zod` (broader ecosystem) or `Valibot` (smaller bundle)
- **Bundle size is the dominant constraint** — even Effect Micro adds tens of KB
- **The team isn't sold on the paradigm shift** — Effect is "almost a language" and shows up everywhere once adopted

## Alternatives

| Need | Pick |
|---|---|
| Just typed errors | **neverthrow** or **ts-results** |
| Functional toolkit, no effect tracking | **fp-ts** (now in maintenance — Effect is the successor) |
| Schema validation only | **Zod** or **Valibot** |
| All of: errors + DI + concurrency + observability | **Effect** |
| Effect with smaller surface | **Effect Micro** |

Decision compass:
- **Greenfield service, team willing to invest** → Effect pays back well
- **Mostly Promise-based codebase, a few rough edges** → `neverthrow` first
- **Just want better validation than Joi/Yup** → Zod
- **Need OTel + retries + structured concurrency anyway** → Effect saves you from gluing 5 libs

## See also

- [best-practices](best-practices.md) — surgical vs all-in adoption strategies
- [error-handling](error-handling.md) — failure vs defect distinction is what makes the boundary tricky
- Official [Effect vs neverthrow](https://effect.website/docs/additional-resources/effect-vs-neverthrow/), [Effect vs fp-ts](https://effect.website/docs/additional-resources/effect-vs-fp-ts/), [Effect vs Promise](https://effect.website/docs/additional-resources/effect-vs-promise/) comparisons
