# Server: handlers, context, registration, streaming, middleware

## Table of contents

- [Service trait shape](#service-trait-shape)
- [RequestContext](#requestcontext)
- [OwnedView and views](#ownedview-and-views)
- [Response builder](#response-builder)
- [Registration](#registration)
- [Streaming RPCs](#streaming-rpcs)
- [Tower middleware via Axum](#tower-middleware-via-axum)
- [Passing data from middleware to handlers](#passing-data-from-middleware-to-handlers)

For testing handlers in isolation and over the wire, see `testing.md`.
For tonic migrations, see `migration-tonic.md`.

For exact trait signatures, sealed traits, and feature gates, fetch
<https://docs.rs/connectrpc/latest/connectrpc/>. See SKILL.md "Compatibility"
for the pinned versions this skill targets.

## Service trait shape

`connectrpc-build` emits one trait per `service` block in your `.proto`. Each
RPC becomes an `async fn`. Implement the trait on a struct that owns your
shared state:

```rust
impl GreetService for MyGreet {
    async fn greet(
        &self,
        ctx: RequestContext,
        req: OwnedView<GreetRequestView<'static>>,
    ) -> ServiceResult<GreetResponse> { /* ... */ }
}
```

Keep `&self` shared across requests — wrap mutable state in `Arc<Mutex<...>>`,
`tokio::sync::RwLock`, or pass an `Arc` to a connection pool. The framework
calls into your handler concurrently from many tasks.

## RequestContext

Carries everything the dispatcher knows about the incoming call:

| Field | Purpose |
|-------|---------|
| `headers` | Caller-supplied request headers (`http::HeaderMap`) |
| `deadline` | Absolute deadline if the client set a timeout |
| `extensions` | `http::Extensions` populated by upstream middleware |

Read deadlines defensively — for long handlers, race them with a `tokio::time::sleep_until` and return `ConnectError::new(ErrorCode::DeadlineExceeded, ...)` rather than letting the dispatcher hang up mid-write.

## OwnedView and views

`OwnedView<TView<'static>>` is the request body. Fields are *borrowed* directly
out of the wire buffer — `req.name: &str` is cheap and allocation-free, but its
lifetime is tied to the view.

Three things to know:

1. **Use as a borrow in the happy path.** `format!("hi {}", req.name)` is fine.
2. **If you need to spawn a task, copy first.** `let name = req.name.to_owned();` then `tokio::spawn(async move { ... use name ... })`.
3. **Convert if you need the owned struct.** `let owned: GreetRequest = req.into_owned();` — costs allocations, but unblocks JSON paths and arbitrary serde.

Do not return views from handlers unless you have measured a bottleneck —
view-bodied responses break JSON clients (see `gotchas.md`).

## Response builder

```rust
Response::ok(GreetResponse { greeting: "hi".into(), ..Default::default() })
    .with_header("x-version", "v2")
    .with_trailer("x-server-id", "node-7")
    .compress(true) // override codec-level compression for this call
```

`Response::ok(msg)` is the common path. `Response::stream_ok(stream)` for
streaming responses. Errors short-circuit via `Err(ConnectError::new(...))` —
do not build a `Response` for the error path.

## Registration

```rust
let svc = Arc::new(MyGreet);
let router = svc.register(Router::new());      // adds POST routes per RPC
let app: axum::Router = router.into_axum_router();
```

Multiple services compose by chaining `.register`:

```rust
let router = greet_svc.register(Router::new());
let router = orders_svc.register(router);
let router = inventory_svc.register(router);
```

Standalone (no Axum): `connectrpc::Server::new(router).serve(addr).await?`. Use
this only when there is no existing HTTP stack to merge into.

**Under the hood**, `register` wires each RPC into the `connectrpc::dispatcher`
machinery (`Dispatcher`, `MethodDescriptor`, `Chain`) for monomorphic dispatch
— that's the type-level path generated code uses. You normally never touch
those types directly; reach for `docs.rs` only if you're reading generated
code or writing your own codec/middleware that hooks into the dispatcher.

## Streaming RPCs

All four kinds (unary, server stream, client stream, bidi) are first-class.
Handler shapes, client-side API, cancellation semantics, and backpressure
have enough subtle behavior that they live in their own file:
**`streaming.md`**. Shape sketch:

```rust
// Server streaming
async fn range(&self, _ctx: RequestContext, req: OwnedView<RangeRequestView<'static>>)
    -> ServiceResult<ServiceStream<RangeResponse>> { /* … */ }

// Client streaming
async fn sum(&self, _ctx: RequestContext, mut requests: ServiceStream<OwnedView<SumRequestView<'static>>>)
    -> ServiceResult<SumResponse> { /* … */ }

// Bidi
async fn running_sum(&self, _ctx: RequestContext, requests: ServiceStream<OwnedView<...>>)
    -> ServiceResult<ServiceStream<RunningSumResponse>> { /* … */ }
```

## Tower middleware via Axum

Compose tower-http and per-RPC concerns at the Axum layer rather than inside
handlers:

```rust
use std::time::Duration;
use axum::Router;
use http::StatusCode;
use tower::ServiceBuilder;
use tower_http::{trace::TraceLayer, timeout::TimeoutLayer, cors::CorsLayer};

let connect = svc.register(Router::new()).into_axum_router();

let app = Router::new()
    .merge(connect)
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(CorsLayer::permissive())
            .layer(axum::middleware::from_fn_with_state(state.clone(), auth_middleware))
            .layer(TimeoutLayer::new(Duration::from_secs(30))),
    );
```

Order matters — outermost layer runs first on the request and last on the
response. Put tracing on the outside so it sees auth failures and timeouts.

## Passing data from middleware to handlers

`RequestContext::extensions` is the same `http::Extensions` that Axum / Tower
middleware writes into. Insert in middleware, read in handler:

```rust
// In middleware
async fn auth_middleware(
    State(tokens): State<TokenStore>,
    mut req: axum::extract::Request,
    next: axum::middleware::Next,
) -> Result<axum::response::Response, StatusCode> {
    let user = verify(&tokens, req.headers()).ok_or(StatusCode::UNAUTHORIZED)?;
    req.extensions_mut().insert(UserId(user));
    Ok(next.run(req).await)
}

// In handler
async fn greet(
    &self,
    ctx: RequestContext,
    _req: OwnedView<GreetRequestView<'static>>,
) -> ServiceResult<GreetResponse> {
    let user = ctx.extensions.get::<UserId>()
        .ok_or_else(|| ConnectError::new(ErrorCode::Unauthenticated, "missing user"))?;
    /* ... */
}
```

This is the same pattern as Axum extractors — there is no separate
"interceptor" abstraction in `connectrpc`. If you've used `tonic`'s
`Interceptor`, this is the equivalent and is more composable.
