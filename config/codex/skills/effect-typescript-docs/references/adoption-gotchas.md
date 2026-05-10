# Adoption Gotchas and Tradeoffs

Use this when evaluating whether to introduce Effect, deciding how much of it to adopt, reviewing a migration, or choosing between Effect and lighter tools. Verify time-sensitive claims against current docs, release notes, and package metadata.

Official docs to check first:
- https://effect.website/docs/getting-started/why-effect/
- https://effect.website/docs/additional-resources/effect-vs-promise/
- https://effect.website/docs/additional-resources/effect-vs-neverthrow/
- https://effect.website/docs/additional-resources/effect-vs-fp-ts/
- https://effect.website/docs/additional-resources/myths/
- https://effect.website/docs/micro/effect-users/
- https://effect.website/docs/micro/new-users/

## Adoption Modes

Surgical adoption:

- Use Schema at trust boundaries.
- Use tagged domain errors in one feature area.
- Keep dependency injection as ordinary function parameters.
- Run Effect only at a narrow boundary.
- Lower onboarding cost and easier rollback.

Effect-native adoption:

- Domain code returns Effect.
- Services are modeled with Context/Layer.
- Resources are scoped.
- A runtime/layer graph is built once per app.
- Retries, concurrency, and observability are composed through Effect.

Pick the mode deliberately. Mixing both without boundaries creates confusing code.

## Boundary Friction

Watch for "Effect tax" around libraries that expect Promise, callback, or exception semantics:

- Web frameworks that route errors through thrown exceptions or `next(err)`.
- Database transactions that rollback only when exceptions escape.
- Error monitoring tools that expect uncaught exceptions.
- Auth middleware and callback-based libraries.
- Streaming libraries with their own lifecycle and cancellation model.

At these seams, decide whether to keep the framework code plain TypeScript and call Effect inside it, or wrap the integration cleanly once. Do not scatter runtime calls through business logic.

## Typechecker and Bundle Risk

Effect-heavy code can increase type inference cost, especially with large layer graphs, deep generated workflows, or very broad union error types.

Mitigations:

- Add explicit return types on exported Effect functions.
- Name intermediate layers and effects.
- Keep service interfaces small.
- Avoid enormous `Effect.gen` blocks.
- Use narrower adoption for browser-shipped code when bundle size matters.

Bundle size and unstable module status change over time. Verify current package metadata and official docs before making claims.

## Alternatives

Choose the smallest tool that solves the real problem:

- Typed result/error only: a result library may be enough.
- Boundary validation only: Zod, Valibot, or Schema depending on project needs.
- Functional utilities without Effect runtime: plain TypeScript or focused FP helpers.
- Full stack of typed errors, services, resources, concurrency, retry, observability, and streams: Effect is a strong fit.

## Code Review Checks

- Is the team/codebase ready for the amount of Effect being introduced?
- Is the first boundary narrow and reversible?
- Are framework seams explicit?
- Is there a validation command that catches type and runtime integration failures?
- Is Effect solving multiple problems, not just adding ceremony around Promise code?
