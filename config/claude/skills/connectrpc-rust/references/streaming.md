# Streaming RPCs: handlers, clients, cancellation, backpressure

All four RPC kinds are first-class. The shapes are predictable once you see
the pattern; the subtleties are around cancellation, client drops, and
backpressure.

## Table of contents

- [The four kinds at a glance](#the-four-kinds-at-a-glance)
- [Server handlers](#server-handlers)
- [Client API by RPC kind](#client-api-by-rpc-kind)
- [ServiceStream — what it is](#servicestream--what-it-is)
- [Cancellation and client drop](#cancellation-and-client-drop)
- [Backpressure](#backpressure)
- [Errors mid-stream](#errors-mid-stream)
- [Graceful drain on shutdown](#graceful-drain-on-shutdown)
- [Streaming over which protocol?](#streaming-over-which-protocol)

## The four kinds at a glance

| RPC kind | Handler input | Handler output | Client send | Client receive |
|----------|---------------|----------------|-------------|-----------------|
| Unary | `OwnedView<ReqView>` | `Response<Resp>` | one `Req` | one response (await) |
| Server stream | `OwnedView<ReqView>` | `ServiceStream<Resp>` | one `Req` | `ServerStream<RespView>` |
| Client stream | `ServiceStream<OwnedView<ReqView>>` | `Response<Resp>` | `impl IntoIterator<Item = Req>` | one response (await) |
| Bidirectional | `ServiceStream<OwnedView<ReqView>>` | `ServiceStream<Resp>` | `.send(req).await` | `BidiStream`: `.message().await` |

## Server handlers

Direct quotes from `examples/streaming-tour/src/server.rs` — the canonical
reference for handler shapes.

**Server streaming** — single request, stream of responses:

```rust
async fn range(
    &self,
    _ctx: RequestContext,
    request: OwnedView<RangeRequestView<'static>>,
) -> ServiceResult<ServiceStream<RangeResponse>> {
    let start = request.start.unwrap_or(0);
    let count = request.count.unwrap_or(0).max(0);
    let stream = futures::stream::iter((0..count).map(move |i| {
        Ok(RangeResponse { value: Some(start + i), ..Default::default() })
    }));
    Response::stream_ok(stream)
}
```

**Client streaming** — stream of requests, single response:

```rust
async fn sum(
    &self,
    _ctx: RequestContext,
    mut requests: ServiceStream<OwnedView<SumRequestView<'static>>>,
) -> ServiceResult<SumResponse> {
    let mut total: i64 = 0;
    while let Some(req) = requests.next().await {
        total += req?.value.unwrap_or(0) as i64;
    }
    Response::ok(SumResponse { total: Some(total), ..Default::default() })
}
```

`requests.next().await` yields `Option<Result<OwnedView<...>, ConnectError>>`.
`None` = client finished sending; `Some(Err(_))` = transport or codec error
mid-stream. Propagate with `?` and the dispatcher returns the error to the
client.

**Bidirectional** — `futures::stream::unfold` is the typical shape:

```rust
async fn running_sum(
    &self,
    _ctx: RequestContext,
    requests: ServiceStream<OwnedView<RunningSumRequestView<'static>>>,
) -> ServiceResult<ServiceStream<RunningSumResponse>> {
    let response_stream =
        futures::stream::unfold((requests, 0i64), |(mut requests, mut total)| async move {
            match requests.next().await? {
                Ok(req) => {
                    total += req.value.unwrap_or(0) as i64;
                    Some((
                        Ok(RunningSumResponse { total: Some(total), ..Default::default() }),
                        (requests, total),
                    ))
                }
                Err(e) => Some((Err(e), (requests, total))),
            }
        });
    Response::stream_ok(response_stream)
}
```

## Client API by RPC kind

**Server streaming** — call returns a `ServerStream`; drain with `.message().await`:

```rust
let mut stream = client.range(RangeRequest {
    start: Some(10), count: Some(5), ..Default::default()
}).await?;
while let Some(msg) = stream.message().await? {
    println!("{}", msg.value.unwrap_or_default());
}
```

`.message()` returns `Ok(None)` when the server is done. After that,
`.trailers()` and `.error()` become available on the stream.

**Client streaming** — pass any `IntoIterator<Item = Req>`:

```rust
let inputs: Vec<SumRequest> = (1..=10).map(|v| SumRequest {
    value: Some(v), ..Default::default()
}).collect();
let resp = client.sum(inputs).await?;
println!("{}", resp.view().total.unwrap_or_default());
```

The transport begins sending as soon as the first envelope is encoded — it
doesn't buffer the whole iterator. Peak memory is roughly
`channel_depth * envelope_size`, not the full body. For lazy generation,
build a `Vec` from an iterator (or `stream::iter` if you have an async
producer and want to fan in via a custom adapter).

**Bidirectional** — explicit `send` / `message` / `close_send`:

```rust
let mut bidi = client.running_sum().await?;
for v in [2, 4, 6, 8] {
    bidi.send(RunningSumRequest { value: Some(v), ..Default::default() }).await?;
    if let Some(msg) = bidi.message().await? {
        println!("running={}", msg.total.unwrap_or_default());
    }
}
bidi.close_send();
// Drain any tail responses:
while let Some(msg) = bidi.message().await? {
    println!("tail={}", msg.total.unwrap_or_default());
}
```

`close_send()` is idempotent and signals end-of-input. **On HTTP/1.1 (Connect
protocol's half-duplex path), you must call `close_send()` before `message()`
will return** — the server cannot start replying until your request body
ends. On HTTP/2 (gRPC, gRPC-Web, Connect streaming over h2), full-duplex
works as expected.

## ServiceStream — what it is

```rust
pub type ServiceStream<T> = Pin<Box<dyn Stream<Item = Result<T, ConnectError>> + Send>>;
```

A boxed `Stream`. Anything implementing `Stream<Item = Result<T, ConnectError>> + Send`
adapts to it — `futures::stream::iter`, `futures::stream::unfold`,
`tokio_stream::wrappers::ReceiverStream`, your own custom impls. Pin in box,
return.

The boxed shape is what the generated trait signatures expect today. Don't
fight it — write the stream however you want, then `Pin::new(Box::new(...))`
or call `Response::stream_ok(stream)` which does the boxing.

## Cancellation and client drop

When the client disconnects mid-call:

1. The transport drops the request body channel.
2. On the handler side, **`requests.next().await` returns `None`** (clean
   close) or `Some(Err(_))` (transport error).
3. The handler's output stream is dropped by the dispatcher.
4. Any `tokio::spawn` started inside the handler keeps running unless you
   tie its lifetime to the handler's. Use `tokio::select!` or a
   `CancellationToken` if the handler kicks off background work that should
   stop on client drop.

The handler future is **not** automatically cancelled on client drop. The
dispatcher detects the disconnect when it tries to write the next response
envelope and the underlying body is gone. If your handler is purely CPU-bound
and never writes, it won't notice until completion.

Defensive pattern for long-running handlers that should stop early:

```rust
let writer = futures::stream::unfold(state, |state| async move {
    // Yield-and-check approach: between items, look at the cancellation signal.
    if state.cancel.is_cancelled() { return None; }
    /* produce next item */
});
```

For unary handlers that need to honor the client's *timeout* header
(separate from drop), race the work against `ctx.deadline`:

```rust
let deadline = ctx.deadline.unwrap_or_else(|| Instant::now() + Duration::from_secs(60));
tokio::select! {
    result = do_work() => Response::ok(result?),
    _ = tokio::time::sleep_until(deadline.into()) => {
        Err(ConnectError::deadline_exceeded("server-side deadline race"))
    }
}
```

## Backpressure

ConnectRPC streaming uses bounded channels (depth 32 between the client send
side and the wire). On HTTP/2, the transport also propagates flow-control
window updates from the peer. The net effect:

- A slow consumer (server reading a client stream, or client reading a server
  stream) **causes the producer's `.send().await` (or yielded item) to await
  longer**.
- `.send()` does not return immediately when the channel is full — it waits
  for room. This is the backpressure handshake.
- `next()` on the receiving side awaits the next envelope; if the producer is
  slow it stays parked until something arrives.

You generally **do not need to add your own buffering**. If you have a
fan-in source that is faster than the network, the bounded channel between
`.send()` and the wire absorbs short bursts and then makes the producer
wait.

## Errors mid-stream

For a stream that has *started* successfully, errors after the first response
envelope come through as `Err` items:

```rust
while let Some(item) = stream.message().await? {
    // `?` on the outer call surfaces transport / protocol errors.
    // The Ok branch is the message.
}
```

For trailing errors (gRPC trailers carry a status), `.message()` returns
`Ok(None)` and you check `.error()` afterward:

```rust
while let Some(msg) = stream.message().await? { /* ... */ }
if let Some(e) = stream.error() {
    return Err(e.clone()); // server-signaled trailing error
}
```

Server-side, returning `Err(_)` from inside the stream produces a trailing
error frame; clients see it as `.error()` after the stream ends.

## Graceful drain on shutdown

When `axum::serve` (or `connectrpc::Server::serve`) shuts down via
`with_graceful_shutdown`, in-flight streams continue until they end naturally.
The accept loop stops taking new connections; existing streams keep their
sockets.

If you need a hard cap on shutdown time, wrap with a timeout:

```rust
let serve = axum::serve(listener, app)
    .with_graceful_shutdown(async { shutdown_signal.await; });

tokio::select! {
    res = serve => res?,
    _ = tokio::time::sleep(Duration::from_secs(30)) => {
        tracing::warn!("graceful shutdown timeout, forcing exit");
    }
}
```

Long-running streams that should self-terminate on shutdown need to listen
for the signal themselves — pass a `CancellationToken` through your service
struct and check it from inside the stream closure.

## Streaming over which protocol?

The same handler serves all three protocols. Client behavior differs:

- **Connect (HTTP/1.1 + JSON or binary):** server streaming and bidi work
  on HTTP/2 only. Client streaming and bidi on HTTP/1.1 are half-duplex —
  the client must close its send side before the server starts responding.
- **gRPC (HTTP/2 only):** full-duplex for bidi.
- **gRPC-Web:** half-duplex; mostly used for browser-side server streaming.

If your `BidiStream` interaction pattern requires the server to respond
between client sends, you must be on HTTP/2 — `HttpClient` negotiates this
automatically for `https://` endpoints with rustls. For `http://`, set
`HttpClient` to use prior-knowledge HTTP/2 if your server supports it; the
default cleartext path is HTTP/1.1.
