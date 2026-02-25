# Crate Composition Guide

## Ecosystem Map

```
┌─────────────────────────────────────────┐
│  Application (async/await)              │
├──────────────┬──────────────────────────┤
│ axum (HTTP)  │  tonic (gRPC)            │
├──────────────┴──────────────────────────┤
│ tower (Service trait, middleware layers) │
├─────────────────────────────────────────┤
│ hyper (HTTP/1.1, HTTP/2)                │
├─────────────────────────────────────────┤
│ tokio (runtime, I/O, sync, timers)      │
├────────────┬───────────┬────────────────┤
│ bytes      │ futures   │ tracing        │
│ (zero-copy)│(combinat.)│(observability) │
└────────────┴───────────┴────────────────┘
```

## Per-Crate Guide

### tokio — The Runtime

The async runtime providing task scheduling, I/O, timers, and sync primitives.

**Core APIs:**
| API | Purpose |
|-----|---------|
| `#[tokio::main]` | Entry point; initializes multi-threaded runtime |
| `tokio::spawn()` | Create lightweight async task → `JoinHandle<T>` |
| `tokio::spawn_blocking()` | Offload blocking/CPU work to thread pool |
| `tokio::time::{sleep, timeout, interval}` | Non-blocking timers |
| `tokio::sync::{mpsc, oneshot, broadcast, watch, Mutex, RwLock, Semaphore}` | Async-aware synchronization |
| `tokio::net::{TcpListener, TcpStream, UdpSocket}` | Async networking |
| `tokio::io::{AsyncRead, AsyncWrite, AsyncBufRead}` | Async I/O traits |

**Anti-patterns:** Using `tokio::sync::Mutex` where `std::sync::Mutex` suffices. Calling `thread::sleep()` instead of `tokio::time::sleep()`. Using `tokio::fs` when `spawn_blocking` + `std::fs` is clearer.

**Docs:** <https://docs.rs/tokio/latest/tokio/>

### futures — Combinators & Utilities

Extends `Future` and `Stream` with method chaining and composition.

**Key traits/macros:**
```rust
use futures::{FutureExt, StreamExt, TryFutureExt, TryStreamExt};

future.map(|x| x * 2);
future.then(|x| async move { ... });
join!(fut1, fut2);
select!(fut1, fut2);
stream.filter(|x| x > 5).take(10).collect().await;
```

**Anti-pattern:** Using `futures::executor::block_on` inside a Tokio runtime → deadlock.

**Docs:** <https://docs.rs/futures/latest/futures/>

### bytes — Zero-Copy Buffers

Reference-counted byte buffers for efficient network I/O.

```rust
// Bytes: immutable, cheaply cloneable (reference-counted)
let data = Bytes::from("hello");
let clone = data.clone(); // shares underlying allocation

// BytesMut: mutable builder
let mut buf = BytesMut::with_capacity(1024);
buf.extend_from_slice(b"data");
let immutable = buf.freeze(); // convert to Bytes
```

**Key traits:** `Buf` (read cursor) and `BufMut` (write cursor) — operations are infallible, unlike `std::io::{Read, Write}`.

**Pairs with:** tokio I/O (`AsyncReadExt::read_buf(&mut BytesMut)`), hyper, tonic.

**Anti-pattern:** Cloning `BytesMut` (expensive copy). Use `Bytes::split_off` for zero-copy sharing.

**Docs:** <https://docs.rs/bytes/latest/bytes/>

### tracing — Structured Observability

Async-aware structured logging with spans and events.

```rust
use tracing::{info, instrument, Instrument};

#[instrument(skip(db))]
async fn fetch_user(id: u64, db: &Database) -> Result<User> {
    info!("Fetching user");
    db.query(id).await
}

// For spawned tasks: attach span explicitly
tokio::spawn(
    async { long_task().await }
        .instrument(tracing::info_span!("bg_job"))
);
```

**Critical rules:**
- Never use `Span::enter()` across `.await` → use `.instrument()` trait instead
- Libraries emit spans/events; executables choose the subscriber (stdout, Jaeger, etc.)
- Use `tracing-subscriber` with `EnvFilter` for log filtering

**Anti-pattern:** Using `log` crate in async code (loses span context across await points).

**Docs:** <https://docs.rs/tracing/latest/tracing/>

### hyper — Low-Level HTTP

HTTP/1.1 and HTTP/2 implementation. Used as the transport layer by axum and tonic.

**Typical usage:** Most applications use **axum** (built on hyper) rather than hyper directly. Use hyper directly only for custom HTTP clients, proxies, or when you need precise control over connection management.

**Docs:** <https://docs.rs/hyper/latest/hyper/>

### tonic — gRPC

Type-safe, async-first gRPC client/server generated from `.proto` files.

```rust
#[tonic::async_trait]
impl Greeter for MyGreeter {
    async fn say_hello(&self, req: Request<HelloRequest>) -> Result<Response<HelloReply>, Status> {
        Ok(Response::new(HelloReply { message: "Hi".into() }))
    }
}
```

**Supports:** Unary, server-streaming, client-streaming, bidirectional streaming RPCs.

**Pairs with:** tower (middleware layers apply to gRPC), tracing, tokio.

**Anti-pattern:** Blocking in gRPC handlers. Not setting deadlines/timeouts. Ignoring streaming backpressure.

**Docs:** <https://docs.rs/tonic/latest/tonic/>

### tower — Service Trait & Middleware

The universal abstraction for request/response services.

```rust
pub trait Service<Request> {
    type Response;
    type Error;
    type Future: Future<Output = Result<Self::Response, Self::Error>>;
    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>>;
    fn call(&mut self, req: Request) -> Self::Future;
}
```

**Key insight:** Tower layers apply identically to HTTP (axum) and gRPC (tonic). Write middleware once, use everywhere.

**Built-in layers:** timeout, rate limit, retry, load balance, concurrency limit.

**Docs:** <https://docs.rs/tower/latest/tower/>

### axum — HTTP Framework

Ergonomic HTTP framework built on hyper + tower. The recommended way to build HTTP APIs in Tokio.

```rust
let app = Router::new()
    .route("/users", get(list_users).post(create_user))
    .route("/users/:id", get(get_user))
    .with_state(Arc::new(app_state))
    .layer(TraceLayer::new_for_http());

let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
axum::serve(listener, app).await?;
```

**Docs:** <https://docs.rs/axum/latest/axum/>

## Composition Rules

1. **tokio + tracing**: Always. Use `#[instrument]` on async functions and `.instrument()` on spawned tasks.
2. **tower + axum/tonic**: Tower layers apply identically to both HTTP and gRPC.
3. **bytes + tokio I/O**: `AsyncReadExt::read_buf(&mut BytesMut)` avoids copies. Never allocate `Vec<u8>` for network buffers.
4. **tokio-stream + mpsc**: `ReceiverStream::new(rx)` converts a channel receiver into a `Stream` for combinator pipelines.

## Architecture Templates

### gRPC Microservice

```
tonic (server/client) + tokio (runtime) + tower (middleware) + tracing (observability)
+ prost (protobuf) + CancellationToken (shutdown) + TaskTracker (drain)
```

### HTTP API Server

```
axum (routing/extractors) + tower-http (trace, timeout, compression, cors)
+ tokio (runtime) + tracing (logging) + std::sync::Mutex or actor pattern (state)
```

### Stream Processing Pipeline

```
tokio channels (mpsc bounded) + tokio-stream (StreamExt combinators)
+ chunks_timeout (micro-batching) + buffer_unordered (concurrent writes)
```
