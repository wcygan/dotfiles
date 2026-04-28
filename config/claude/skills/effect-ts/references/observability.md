# Observability

## Contents
- Structured logging
- Tracing with `Effect.withSpan`
- Metrics
- OpenTelemetry export
- Annotations and FiberRefs

## Structured logging

Logging is built into the runtime — no extra package needed:

```ts
import { Effect } from "effect"

Effect.gen(function* () {
  yield* Effect.log("started")                          // INFO level
  yield* Effect.logDebug("with detail", { foo: 1 })
  yield* Effect.logInfo("processed", { count: 5 })
  yield* Effect.logWarning("slow")
  yield* Effect.logError("failed", err)
})
```

Log entries automatically include:
- Timestamp
- Fiber ID
- Active span (if any) — logs become span events
- Annotations from `Effect.annotateLogs`
- Caller location (from cause)

Annotate a region:

```ts
const handler = (req: Request) => myEffect.pipe(
  Effect.annotateLogs("requestId", req.headers.get("x-request-id"))
)
```

Switch logger format/destination:

```ts
import { Logger, LogLevel } from "effect"

const program = myEffect.pipe(
  Logger.withMinimumLogLevel(LogLevel.Debug),
  Effect.provide(Logger.json)              // emit JSON instead of pretty
)
```

## Tracing with `Effect.withSpan`

`Effect.withSpan` wraps a piece of work in an OpenTelemetry-compatible span:

```ts
const charge = (cents: number) =>
  Effect.gen(function* () {
    yield* validate(cents)
    yield* postToStripe(cents)
  }).pipe(
    Effect.withSpan("charge", {
      attributes: { "billing.cents": cents }
    })
  )
```

Nested spans automatically chain. Failures attach error information. Logs in the span's lifetime become span events.

## Metrics

```ts
import { Metric, Effect } from "effect"

const requestsCounter = Metric.counter("requests_total", { description: "..." })
const responseLatency = Metric.histogram("response_seconds",
  MetricBoundaries.exponential({ start: 0.001, factor: 2, count: 10 })
)
const inFlight = Metric.gauge("requests_in_flight")

const handler = myEffect.pipe(
  Metric.increment(requestsCounter),         // bump by 1
  Effect.timed,                              // [Duration, A]
  Effect.tap(([d]) => Metric.update(responseLatency, Duration.toSeconds(d)))
)
```

## OpenTelemetry export

Install `@effect/opentelemetry`:

```ts
import { NodeSdk } from "@effect/opentelemetry"
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http"
import { BatchSpanProcessor } from "@opentelemetry/sdk-trace-base"

const TracingLive = NodeSdk.layer(() => ({
  resource: { serviceName: "my-app" },
  spanProcessor: new BatchSpanProcessor(new OTLPTraceExporter())
}))

const AppLive = Layer.mergeAll(/* ... */, TracingLive)
```

Now every `Effect.withSpan` exports to your OTel collector (Tempo, Honeycomb, Datadog, etc.). Layer-built services that use `Effect.withSpan` internally (like an HTTP client) propagate traces automatically.

## Annotations and FiberRefs

Use `FiberRef` to thread context through fibers — like AsyncLocalStorage but structured:

```ts
const RequestId = FiberRef.make<string>("unknown")

const program = Effect.gen(function* () {
  yield* FiberRef.set(RequestId, req.id)
  yield* doWork
}).pipe(Effect.scoped)

// inside doWork:
const id = yield* FiberRef.get(RequestId)
```

`Effect.annotateLogs` and `Effect.annotateSpans` are sugar for FiberRefs scoped to the logging/tracing systems.

## See also

- [services-and-layers](services-and-layers.md) — `Logger`, `Tracer` are services
- [runtime-and-execution](runtime-and-execution.md) — `ManagedRuntime` flushes telemetry on dispose
- [error-handling](error-handling.md) — `Cause.pretty` for human-readable failure
