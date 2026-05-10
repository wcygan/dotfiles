# Streams, Platform, and Observability

Use this when working with Stream, Sink, platform APIs, command/file/path/terminal abstractions, logging, metrics, tracing, supervision, or telemetry export. Verify exact APIs in the official docs or installed package exports before editing.

Official docs to check first:
- https://effect.website/docs/stream/introduction/
- https://effect.website/docs/stream/creating/
- https://effect.website/docs/stream/consuming-streams/
- https://effect.website/docs/stream/error-handling/
- https://effect.website/docs/stream/resourceful-streams/
- https://effect.website/docs/sink/introduction/
- https://effect.website/docs/platform/introduction/
- https://effect.website/docs/platform/file-system/
- https://effect.website/docs/platform/command/
- https://effect.website/docs/observability/logging/
- https://effect.website/docs/observability/metrics/
- https://effect.website/docs/observability/tracing/
- https://effect.website/docs/observability/supervisor/

## Stream vs Effect

Use `Effect` for one result. Use `Stream` when the program naturally emits many values over time or needs stream-specific behavior:

- Backpressure.
- Chunked processing.
- Incremental consumption.
- Infinite or long-running feeds.
- Resourceful pipelines.
- Stream-specific error handling.

If a task only maps an array or makes a few independent calls, `Effect.forEach` or equivalent may be simpler than introducing Stream.

## Sink

Use Sink when consumption itself is reusable or stateful:

- Folding stream elements into a summary.
- Taking a prefix and leaving leftovers.
- Validating or parsing a stream protocol.
- Sharing a consumption strategy across multiple streams.

Do not add Sink just to collect a stream once if a direct stream consumer is clearer.

## Platform APIs

`@effect/platform` is useful when the codebase wants cross-runtime abstractions for files, paths, commands, terminal IO, key-value storage, or runtime integration.

Before introducing platform packages:

- Check whether the project already depends on them.
- Confirm the target runtime: Node, Bun, Deno, browser, worker, or Tauri.
- Verify package names and module status in current docs.
- Keep framework-specific wiring in the framework layer; keep domain logic runtime-agnostic when possible.

## Observability

Effect can carry logs, metrics, spans, annotations, and fiber-local context through the program. Use observability at meaningful boundaries:

- Request, job, command, or workflow spans.
- Retry and timeout counters.
- Failure/defect cause logging at edges.
- Service-level annotations such as request id, user id, or correlation id.

Do not add noisy spans to every tiny helper. Prefer spans that would help debug latency, fanout, retries, or external service calls.

## Code Review Checks

- Is Stream justified by multi-value, backpressure, or resourceful processing needs?
- Are resourceful streams scoped correctly?
- Is platform usage consistent with the runtime and installed packages?
- Are logs/metrics/traces added at useful boundaries rather than everywhere?
- Are defects logged with enough cause detail without exposing secrets?
