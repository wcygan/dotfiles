---
name: effect-typescript-docs
description: Use when building, reviewing, debugging, or migrating Effect TypeScript code and needing idiomatic implementation guidance backed by current official docs. Trigger for Effect, effect/Schema, Effect.gen, pipe, Runtime, ManagedRuntime, Layer, Context.Tag, Config, Scope, Schedule, Stream, Sink, Queue, PubSub, Fiber, Cause, Exit, Option, Either, Effect AI, @effect/platform, Micro, or TypeScript imports from the `effect` ecosystem.
---

# Effect TypeScript Docs

Use this skill to produce idiomatic Effect TypeScript implementation guidance while verifying current API details against official docs and the installed project version.

## Operating Model

Keep this model in mind before choosing patterns:

```ts
Effect.Effect<A, E, R>
```

- `A`: success value.
- `E`: expected, recoverable failure type.
- `R`: required services that must be provided before execution.
- Effects are lazy descriptions. They run only when a runtime executes them.
- Run effects at program edges: HTTP handlers, CLIs, workers, tests, scheduled jobs.
- Use typed failures for domain outcomes and defects for bugs or impossible states.
- Prefer `Effect.gen` for sequential business logic and `pipe` for short transforms.

## Workflow

1. Identify the task: explain, design, migrate Promise code, fix a type error, implement a feature, review Effect code, or evaluate adoption.
2. Inspect local context before editing: `package.json`, lockfile, installed `effect` version when available, TypeScript config, imports, nearby style, and tests.
3. Load the smallest relevant reference file from the map below for idioms and tradeoffs.
4. Use `references/doc-map.md` to choose official docs when the right page is not obvious.
5. Fetch the current official page from `https://effect.website/docs/...` before making precise claims about APIs, signatures, examples, or recommended patterns.
6. Use the API list or installed package exports when exact functions, methods, overloads, or module members matter.
7. Make changes in the project's existing style. Match import style, package manager, test framework, Effect version, and boundary conventions.
8. Verify with the narrowest meaningful local command first: typecheck, targeted tests, affected build, or package-specific checks.

## Quick Decisions

- Sequential effectful workflow: use `Effect.gen`.
- Short transformation or recovery chain: use `pipe`.
- Domain error with fields: use a tagged error pattern, then recover by tag.
- Thrown sync/Promise API: wrap it and map thrown values into typed failures.
- HTTP, CLI, queue, or worker boundary: provide services and run once at the edge.
- Reused app services such as DB pools or telemetry: build layers/runtime once, not per operation.
- Need all parallel results: use structured concurrency helpers with explicit concurrency.
- Need first winner or cancellation signal: race deliberately and confirm loser interruption semantics.
- Resource with acquire/release: use scoped resource management.
- Boundary validation or wire encoding: use Schema; verify exact constructors and decode/encode helpers in docs.
- Only need typed errors or only need validation: consider lighter alternatives before expanding Effect across the codebase.

## Navigation Heuristics

- New projects, imports, creating/running effects, generator syntax, pipelines, and control flow: start with Getting Started.
- Error modeling, recovery, defects, accumulation, retry, timeout, sandboxing, `Cause`, `Exit`, `Either`, or yieldable errors: start with Error Management and Data Types.
- Dependency injection, services, `Context`, `Layer`, default services, configuration, runtime provisioning, or app bootstrapping: start with Requirements Management, Configuration, and Runtime.
- Resource safety, acquisition/release, finalizers, or scoped lifetimes: start with Resource Management and `Scope`.
- Concurrency, interruption, racing, `Fiber`, `Queue`, `PubSub`, `Deferred`, `Latch`, or `Semaphore`: start with Concurrency.
- Validation, parsing, encoding, transformations, JSON Schema, branded schemas, class APIs, or pretty/error formatting: start with Schema.
- Streaming pipelines, stream creation/consumption, stream errors, leftovers, or `Sink`: start with Stream and Sink.
- Caching, batching, schedules, cron, repetition, retries, or polling: start with Caching, Batching, and Scheduling.
- Files, paths, commands, terminal IO, key-value storage, or cross-platform runtime APIs: start with Platform.
- Logging, metrics, tracing, or supervision: start with Observability.
- Comparisons, migration, or evaluating adoption: start with Additional Resources.

## Reference Map

- `references/fundamentals.md`: `Effect<A, E, R>`, laziness, constructors, generator vs pipe style, running at the edge.
- `references/errors-runtime.md`: expected failures vs defects, tagged errors, recovery, `Exit`, `Cause`, edge routing.
- `references/services-layers.md`: services, `Context.Tag`, `Layer`, `Config`, test doubles, runtime placement.
- `references/schema.md`: Schema as boundary validation, decode/encode, brands, transformations, derived artifacts.
- `references/concurrency-resources-scheduling.md`: structured concurrency, fibers, queues, scopes, resource safety, schedules, retries, timeouts.
- `references/streams-platform-observability.md`: Stream/Sink choice, platform APIs, logging, metrics, tracing, supervision.
- `references/adoption-gotchas.md`: incremental adoption, boundary friction, bundle/typechecker risk, alternatives.
- `references/doc-map.md`: official docs navigation index generated from `https://effect.website/llms.txt`, grouped by docs area with the API list link.

## Quality Rules

- Prefer official Effect docs over memory. Local references are idiom guides, not API snapshots.
- Do not invent API names from familiarity with older Effect versions. Verify exact names in official docs, the API list, or installed package exports.
- Keep examples idiomatic for the project in front of you: match its import style, package manager, test framework, and Effect version.
- When docs and local package behavior conflict, call out the mismatch and trust the installed version for code changes.
- Keep `R` honest. Do not suppress missing service requirements with `as any`.
- Avoid running effects inside business logic just to escape the type system.
- Treat framework integration as a boundary design problem. Keep plain framework code plain when that is simpler; convert to/from Effect deliberately.
- For time-sensitive claims such as v4 status, package splits, unstable modules, or current bundle size, verify current docs or release notes first.
- Keep quotes short; summarize docs rather than copying full examples or long passages.
