# anomalyco/opencode Effect Examples

Snapshot: `69cfc44dba32b37aeadd13c5f4cf243967d9f346` on the `dev` branch, inspected 2026-06-04.

Use these examples for production Effect usage in a CLI/agent backend: service layers, schemas, typed failures, platform IO, streams, process management, and retry policies.

## High-Level Read

opencode treats Effect as an application substrate rather than a single helper library. The codebase uses `Schema` for API and event boundaries, `Context.Service` plus `Layer` for long-lived services, `Stream` for LLM and process output, and `Schedule` for retry decisions. This is a good repo to study when the problem is "many unreliable external systems need one typed runtime model": LLM providers, MCP servers, child processes, local databases, HTTP APIs, and background session state.

The main adoption pattern is service-oriented: define a domain service interface, construct it with `Layer.effect`, pull dependencies from `R`, and expose methods that return lazy `Effect` values. Effects are run near CLI/server/runtime edges, not inside pure business helpers.

## Permalinks

- [MCP schemas, tagged errors, and status union](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/mcp/index.ts#L30-L100) - boundary schemas and typed MCP status modeling.
- [MCP remote connection workflow](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/mcp/index.ts#L306-L390) - `Effect.fn`, OAuth control flow, `Effect.catch`, and typed status recovery.
- [MCP OAuth start/auth flow](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/mcp/index.ts#L782-L840) - wrapping Promise APIs with `Effect.tryPromise`, recovering expected auth failures, and dying on defects.
- [Installation service definition](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/installation/index.ts#L1-L103) - `Schema`, tagged errors, `Context.Service`, `Layer.effect`, and `@effect/platform` HTTP/process dependencies.
- [Installation latest-version checks](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/installation/index.ts#L221-L277) - schema-decoded HTTP responses from npm, Homebrew, Chocolatey, Scoop, and GitHub.
- [LLM service layer and requirements](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/session/llm.ts#L54-L85) - service interface plus `Layer.effect` that pulls required services from `R`.
- [LLM streaming with scoped abort controller](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/session/llm.ts#L355-L379) - `Stream.scoped`, `Effect.acquireRelease`, and async-iterable stream adaptation.
- [Session processor stream drain and retry](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/session/processor.ts#L943-L970) - streaming events, interruption handling, cause filtering, and retry policy integration.
- [Project service process execution](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/project/project.ts#L113-L162) - typed service methods, scoped child process spawning, concurrent stdout/stderr collection, and fallback recovery.
- [Custom session retry schedule](https://github.com/anomalyco/opencode/blob/69cfc44dba32b37aeadd13c5f4cf243967d9f346/packages/opencode/src/session/retry.ts#L176-L199) - `Schedule.fromStepWithMetadata`, current time, custom delay calculation, and retry-status side effects.

## Code Samples

These are distilled pattern sketches from the linked code, not verbatim excerpts.

### Service + Layer

```ts
import { Context, Effect, Layer } from "effect"

interface Installation {
  readonly latest: () => Effect.Effect<string>
  readonly upgrade: (target: string) => Effect.Effect<void, UpgradeFailedError>
}

class InstallationService extends Context.Service<InstallationService, Installation>()(
  "@app/Installation"
) {}

const installationLayer = Layer.effect(
  InstallationService,
  Effect.gen(function* () {
    const http = yield* HttpClient.HttpClient
    const appProcess = yield* AppProcess.Service

    return InstallationService.of({
      latest: () => fetchLatestVersion(http),
      upgrade: (target) => runUpgrade(appProcess, target),
    })
  })
)
```

### Schema-Decoded HTTP Boundary

```ts
import { Effect, Schema } from "effect"

const NpmPackage = Schema.Struct({ version: Schema.String })

const latestFromRegistry = Effect.gen(function* () {
  const response = yield* httpOk.execute(
    HttpClientRequest.get("https://registry.example.com/pkg/latest").pipe(
      HttpClientRequest.acceptJson
    )
  )

  const body = yield* HttpClientResponse.schemaBodyJson(NpmPackage)(response)
  return body.version
})
```

### Scoped Stream With Abort Cleanup

```ts
const streamLlmEvents = (input: StreamInput) =>
  Stream.scoped(
    Stream.unwrap(
      Effect.gen(function* () {
        const controller = yield* Effect.acquireRelease(
          Effect.sync(() => new AbortController()),
          (controller) => Effect.sync(() => controller.abort())
        )

        const result = yield* runLlm({ ...input, abort: controller.signal })
        return Stream.fromAsyncIterable(result.fullStream, normalizeError)
      })
    )
  )
```

### Stream Processing With Retry Policy

```ts
const processSession = Effect.gen(function* () {
  yield* llm.stream(input).pipe(
    Stream.tap(handleEvent),
    Stream.takeUntil(() => state.needsCompaction),
    Stream.runDrain,
    Effect.onInterrupt(markAborted),
    Effect.retry(sessionRetryPolicy)
  )
})
```
