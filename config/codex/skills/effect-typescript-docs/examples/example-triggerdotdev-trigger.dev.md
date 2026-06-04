# triggerdotdev/trigger.dev Effect Examples

Snapshot: `4ea3ef138febc66999785afdcd17e056e65a5e21` on the `main` branch, inspected 2026-06-04.

Use these examples for narrow, pragmatic Effect adoption inside a larger TypeScript app: background loops, fibers, retry, Promise wrapping, optimistic locking, and Effect Schema interoperability.

## High-Level Read

Trigger.dev is the best contrast case in this set because Effect is not the whole architecture. It appears around workflows where ordinary async code gets awkward: a background metadata flush loop, lifecycle-managed fibers, retry with backoff, Promise-heavy database calls, and schema conversion support. The surrounding code remains conventional TypeScript classes, Prisma calls, tests, and utility functions.

Study this repo when considering incremental adoption. The useful pattern is to wrap the hard workflow in Effect, run it at the boundary with `runFork` or `runPromise`, and keep the rest of the application plain unless it benefits from typed errors, retry, interruption, or schema interoperability.

## Permalinks

- [Effect imports for metadata service](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/apps/webapp/app/services/metadata/updateMetadata.server.ts#L1-L40) - `Effect`, `Schedule`, `Duration`, `Fiber`, and `RuntimeFiber` introduced into an otherwise ordinary service class.
- [Background flushing loop](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/apps/webapp/app/services/metadata/updateMetadata.server.ts#L60-L103) - `Effect.gen`, `Effect.sleep`, sync logging, catch-all containment, and `Effect.runFork`.
- [Fiber interruption on shutdown](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/apps/webapp/app/services/metadata/updateMetadata.server.ts#L101-L109) - stores a runtime fiber and interrupts it from a plain class method.
- [Buffered operations with retry](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/apps/webapp/app/services/metadata/updateMetadata.server.ts#L111-L165) - `Effect.catchIf`, `Effect.retry`, exponential schedule, and re-buffering on complete failure.
- [Prisma and packet parsing wrapped in Effect](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/apps/webapp/app/services/metadata/updateMetadata.server.ts#L170-L250) - `Effect.tryPromise`, `Effect.try`, typed failure flow, and optimistic-lock update predicates.
- [Manual flush boundary](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/apps/webapp/app/services/metadata/updateMetadata.server.ts#L552-L559) - converts the internal effectful workflow back to a Promise for an imperative testing/ops method.
- [Multi-library schema conversion entrypoint](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/packages/schema-to-json/src/index.ts#L1-L80) - adds Effect JSON Schema support beside Zod, ArkType, TypeBox, Valibot, and Yup style schema handling.
- [Effect Schema detection and conversion](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/packages/schema-to-json/src/index.ts#L163-L172) - detects Effect schemas by AST shape and converts with `EffectJSONSchema.make`.
- [Effect Schema conversion tests](https://github.com/triggerdotdev/trigger.dev/blob/4ea3ef138febc66999785afdcd17e056e65a5e21/packages/schema-to-json/tests/index.test.ts#L162-L197) - verifies `Schema.Struct` conversion, required fields, and optional fields.

## Code Samples

These are distilled pattern sketches from the linked code, not verbatim excerpts.

### Background Loop In A Plain Class

```ts
import { Duration, Effect, Fiber } from "effect"
import type { RuntimeFiber } from "effect/Fiber"

class MetadataFlusher {
  private fiber: RuntimeFiber<void> | null = null

  start() {
    const program = Effect.gen(this, function* () {
      while (true) {
        yield* Effect.sleep(Duration.millis(this.flushIntervalMs))
        const batch = this.takeBufferedOperations()

        if (batch.size > 0) {
          yield* this.processBufferedOperations(batch)
        }
      }
    }).pipe(Effect.catchAll((error) => Effect.sync(() => this.logger.error(error))))

    this.fiber = Effect.runFork(program as Effect.Effect<void, never, never>)
  }

  stop() {
    if (this.fiber) Effect.runFork(Fiber.interrupt(this.fiber))
  }
}
```

### Retry With Special-Case Recovery

```ts
const processRun = (runId: string, operations: MetadataOperation[]) =>
  updateRunWithOperations(runId, operations).pipe(
    Effect.catchIf(
      (error) => error instanceof MetadataTooLargeError,
      (error) => Effect.sync(() => logger.warn("dropping large metadata", { error }))
    ),
    Effect.retry(Schedule.exponential(Duration.millis(100), 1.4)),
    Effect.catchAll((error) =>
      Effect.sync(() => {
        rebuffer(runId, operations)
        logger.error("failed metadata flush", { error })
      })
    )
  )
```

### Promise APIs Inside A Typed Workflow

```ts
const updateRunWithOperations = (runId: string, operations: Operation[]) =>
  Effect.gen(function* () {
    const run = yield* Effect.tryPromise(() =>
      prisma.taskRun.findFirst({ where: { id: runId } })
    )

    if (!run) return yield* Effect.fail(new Error(`Run ${runId} not found`))

    const packet = yield* Effect.try(() => parseMetadataPacket(run.metadata))
    const next = applyMetadataOperations(packet, operations)

    return yield* Effect.tryPromise(() =>
      prisma.taskRun.updateMany({
        where: { id: runId, metadataVersion: run.metadataVersion },
        data: { metadata: next, metadataVersion: { increment: 1 } },
      })
    )
  })
```

### Effect Schema To JSON Schema Adapter

```ts
import { JSONSchema as EffectJSONSchema } from "effect"

function isEffectSchema(schema: unknown): boolean {
  const candidate = schema as { ast?: { _tag?: unknown } }
  return typeof candidate.ast === "object" && typeof candidate.ast?._tag === "string"
}

function convertEffectSchema(schema: unknown): JSONSchema | undefined {
  try {
    return EffectJSONSchema.make(schema) as JSONSchema
  } catch {
    return undefined
  }
}
```
