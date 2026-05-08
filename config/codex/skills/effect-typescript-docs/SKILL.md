---
name: effect-typescript-docs
description: Use when working with Effect in TypeScript and needing official documentation navigation, API lookup, or implementation guidance. Trigger for Effect, effect/Schema, Effect Runtime, Layers, Services, Config, Scope, Schedule, Stream, Sink, Queue, PubSub, Fiber, Cause, Exit, Option, Either, Effect AI, @effect/platform, Micro, or when modifying TypeScript code that imports from the `effect` ecosystem.
---

# Effect TypeScript Docs

Use this skill to route Effect TypeScript questions to the right official docs before giving implementation advice or editing code.

## Workflow

1. Identify the Effect topic in the user request or existing TypeScript imports.
2. Read `references/doc-map.md` only when the right official page is not obvious.
3. Fetch the current official page from `https://effect.website/docs/...` before making precise claims about APIs, signatures, examples, or recommended patterns.
4. Use the API list when exact functions, methods, or module members matter.
5. Verify against the local project when editing code: inspect `package.json`, installed `effect` package version, existing imports, and nearby code patterns.

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

## Quality Rules

- Prefer official Effect docs over memory. The bundled reference is only a navigation aid.
- Do not invent API names from familiarity with older Effect versions. Verify exact names in the docs, API list, or installed package exports.
- Keep examples idiomatic for the project in front of you: match its import style, package manager, test framework, and Effect version.
- When docs and local package behavior conflict, call out the mismatch and trust the installed version for code changes.
- Keep quotes short; summarize docs rather than copying full examples or long passages.

## Reference Map

- `references/doc-map.md`: local navigation index generated from `https://effect.website/llms.txt`, grouped by docs area with the API list link.
