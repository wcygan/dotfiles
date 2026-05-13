# Migrating from tonic

You know tonic. Here is what changes — and what stays — when porting a
service to `connectrpc`. Codegen swap, handler signatures, error
translation, transport, client construction.

## Table of contents

- [Mental model deltas](#mental-model-deltas)
- [Cargo.toml swap](#cargotoml-swap)
- [Codegen (build.rs)](#codegen-buildrs)
- [Service trait + handler signatures](#service-trait--handler-signatures)
- [Errors: Status → ConnectError](#errors-status--connecterror)
- [Interceptors → Tower / Axum middleware](#interceptors--tower--axum-middleware)
- [Server entrypoint](#server-entrypoint)
- [Client construction](#client-construction)
- [Streaming](#streaming)
- [What you lose](#what-you-lose)
- [What you gain](#what-you-gain)

## Mental model deltas

| Concept | tonic | connectrpc |
|---------|-------|------------|
| Service trait | `#[tonic::async_trait]` decorated | Plain `async fn` (Rust 2024 edition) |
| Request type | `tonic::Request<T>` | `(RequestContext, OwnedView<TView<'static>>)` |
| Response type | `tonic::Response<T>` | `Response<T>` (from `connectrpc::Response`) |
| Server entrypoint | `Server::builder().add_service(...).serve(addr)` | `service.register(Router::new()).into_axum_router()` + `axum::serve` |
| Interceptors | `tonic::Interceptor` trait | Axum / Tower middleware via `http::Extensions` |
| Error type | `tonic::Status` | `ConnectError` (same code set, different name) |
| Streaming type | `tonic::Streaming<T>` | `ServiceStream<T>` |
| Codegen | `tonic-build` + `prost-build` | `connectrpc-build` (bundles `buffa-codegen`) |
| Message types | `prost::Message` derive | `buffa` owned struct + `TView<'a>` zero-copy view |
| Transport feature | `transport` (default) | `axum` + `client` + `client-tls` / `server-tls` (granular) |
| Protocols served | gRPC (HTTP/2 only) | Connect + gRPC + gRPC-Web on one server |

The biggest conceptual shift: **tonic owns its transport stack; connectrpc
plugs into yours.** You bring the `axum::Router` and the `tower-http` layers.

## Cargo.toml swap

Out:

```toml
[dependencies]
tonic = "0.12"
prost = "0.13"
tokio = { version = "1", features = ["full"] }

[build-dependencies]
tonic-build = "0.12"
```

In:

```toml
[dependencies]
connectrpc = { version = "0.4", features = ["axum", "client", "tls"] }
axum = "0.8"
tokio = { version = "1", features = ["full"] }

[build-dependencies]
connectrpc-build = "0.4"
```

You do **not** need `prost` or `buffa` as direct deps — they come in through
`connectrpc` and `connectrpc-build`.

## Codegen (build.rs)

Tonic:

```rust
fn main() {
    tonic_build::configure()
        .compile_protos(&["proto/greet.proto"], &["proto/"])
        .unwrap();
}
```

ConnectRPC:

```rust
fn main() {
    connectrpc_build::Config::new()
        .files(&["proto/greet.proto"])
        .includes(&["proto/"])
        .include_file("_connectrpc.rs")
        .compile()
        .unwrap();
}
```

Then in your crate:

```rust
include!(concat!(env!("OUT_DIR"), "/_connectrpc.rs"));
```

`include_file` is the convenience knob tonic doesn't have — it collects every
generated module into one file you `include!` once. Without it, you'd
`include!` per-proto.

Both still need `protoc` on PATH (v27+ for `connectrpc-build`). See
`codegen.md` for `buf generate` and standalone-`protoc` alternatives.

## Service trait + handler signatures

Tonic:

```rust
use tonic::{Request, Response, Status};

#[tonic::async_trait]
impl GreetService for MyGreet {
    async fn greet(
        &self,
        request: Request<GreetRequest>,
    ) -> Result<Response<GreetResponse>, Status> {
        let name = &request.into_inner().name;
        Ok(Response::new(GreetResponse {
            greeting: format!("hi {name}"),
        }))
    }
}
```

ConnectRPC:

```rust
use connectrpc::{RequestContext, Response, ServiceResult};
use buffa::view::OwnedView;

impl GreetService for MyGreet {
    async fn greet(
        &self,
        _ctx: RequestContext,
        req: OwnedView<GreetRequestView<'static>>,
    ) -> ServiceResult<GreetResponse> {
        Response::ok(GreetResponse {
            greeting: Some(format!("hi {}", req.name.unwrap_or(""))),
            ..Default::default()
        })
    }
}
```

Three things changed:

1. **No `#[tonic::async_trait]`.** Rust 2024 supports `async fn` in traits
   natively.
2. **Request is split into `(ctx, body)`.** `ctx` is metadata + extensions
   (the tonic `Request<T>::metadata()` / `extensions()` analogue); the body
   is a zero-copy view of the proto.
3. **Buffa fields are `Option<T>` for scalars** (edition-2023 default-presence
   semantics). `unwrap_or(default)` is the unset-treated-as-zero analogue of
   prost's bare scalar fields.

Return owned messages by default. The `OwnedView` request input is *not* the
same direction as the response — you can absolutely return views too, but
that path breaks JSON clients (see `gotchas.md`).

## Errors: Status → ConnectError

Both speak the same canonical code set; only the type name differs.

```rust
// Tonic
return Err(Status::permission_denied("workload not allowed"));

// ConnectRPC — verbose
return Err(ConnectError::new(ErrorCode::PermissionDenied, "workload not allowed"));

// ConnectRPC — there are constructors for each code:
return Err(ConnectError::permission_denied("workload not allowed"));
```

Code mapping (1:1, name parity):

| tonic `Status::*` | `ConnectError` constructor | `ErrorCode::*` |
|-------------------|---------------------------|-----------------|
| `cancelled` | `canceled` | `Canceled` |
| `unknown` | `unknown` | `Unknown` |
| `invalid_argument` | `invalid_argument` | `InvalidArgument` |
| `deadline_exceeded` | `deadline_exceeded` | `DeadlineExceeded` |
| `not_found` | `not_found` | `NotFound` |
| `already_exists` | `already_exists` | `AlreadyExists` |
| `permission_denied` | `permission_denied` | `PermissionDenied` |
| `resource_exhausted` | `resource_exhausted` | `ResourceExhausted` |
| `failed_precondition` | `failed_precondition` | `FailedPrecondition` |
| `aborted` | `aborted` | `Aborted` |
| `out_of_range` | `out_of_range` | `OutOfRange` |
| `unimplemented` | `unimplemented` | `Unimplemented` |
| `internal` | `internal` | `Internal` |
| `unavailable` | `unavailable` | `Unavailable` |
| `data_loss` | `data_loss` | `DataLoss` |
| `unauthenticated` | `unauthenticated` | `Unauthenticated` |

`ErrorDetail` (structured error payloads) replaces `Status::with_details` —
see `errors.md` for the shape.

## Interceptors → Tower / Axum middleware

Tonic's `Interceptor` is a wrapper around `tower::Service`, but most users
hit it via the trait sugar:

```rust
// Tonic
let svc = GreetServer::with_interceptor(MyGreet, auth_interceptor);
```

In connectrpc there is no separate interceptor concept — you write a plain
Axum middleware that inserts into `http::Extensions`, and the handler reads
it from `ctx.extensions`:

```rust
async fn auth_middleware(
    State(tokens): State<TokenStore>,
    mut req: axum::extract::Request,
    next: axum::middleware::Next,
) -> Result<axum::response::Response, StatusCode> {
    let user = verify(&tokens, req.headers()).ok_or(StatusCode::UNAUTHORIZED)?;
    req.extensions_mut().insert(UserId(user));
    Ok(next.run(req).await)
}

// in main():
let app = service.register(Router::new())
    .into_axum_router()
    .layer(axum::middleware::from_fn_with_state(state, auth_middleware));

// in the handler:
let user = ctx.extensions.get::<UserId>()
    .ok_or_else(|| ConnectError::unauthenticated("missing user"))?;
```

This is the same pattern tonic users already use for everything *outside*
gRPC. The change here is that ConnectRPC routes go through the same pipeline,
so you have one auth/tracing/timeout setup instead of two.

## Server entrypoint

Tonic:

```rust
Server::builder()
    .add_service(GreetServer::new(MyGreet))
    .add_service(OrdersServer::new(MyOrders))
    .serve("0.0.0.0:8080".parse()?)
    .await?;
```

ConnectRPC:

```rust
let greet = Arc::new(MyGreet);
let orders = Arc::new(MyOrders);

let router = greet.register(Router::new());
let router = orders.register(router);
let app = router.into_axum_router();

let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
axum::serve(listener, app).await?;
```

For TLS, use `connectrpc::axum::serve_tls(listener, app, tls_config)` — the
companion helper (see `compression-tls.md`). Wrapping `axum::serve` with
`tokio_rustls` directly hangs on h2 ALPN.

If you actively want tonic's "owns the transport" shape, the standalone
`connectrpc::Server::new(router).serve(addr)` exists — but use it only when
there's no existing HTTP stack to merge into.

## Client construction

Tonic:

```rust
let channel = Channel::from_static("https://api.example.com").connect().await?;
let mut client = GreetClient::new(channel);
let resp = client.greet(GreetRequest { name: "world".into() }).await?;
println!("{}", resp.into_inner().greeting);
```

ConnectRPC:

```rust
use connectrpc::client::{HttpClient, ClientConfig};

let http = HttpClient::plaintext(); // or HttpClient::with_tls(Arc::new(tls_cfg))
let config = ClientConfig::new("https://api.example.com".parse()?);
let client = GreetServiceClient::new(http, config);

let resp = client.greet(GreetRequest {
    name: Some("world".into()),
    ..Default::default()
}).await?;
println!("{}", resp.view().greeting.unwrap_or(""));
```

`HttpClient` owns the connection pool — build one and clone it across
service clients (cloning is cheap, `Arc` inside). `ClientConfig` carries
default headers and timeouts; per-call overrides go through
`*_with_options` and `CallOptions` (see `client.md`).

## Streaming

`tonic::Streaming<T>` → `connectrpc::ServiceStream<T>`. The API surface
matches `futures::Stream`. Handler signatures take `ServiceStream<OwnedView<...>>`
for client-streaming/bidi inputs and return `ServiceStream<Resp>` for
server-streaming/bidi outputs.

See `streaming.md` for cancellation semantics, backpressure, and the
client-drop story — they differ in subtle ways from tonic.

## What you lose

- **`tonic-health`, `tonic-reflection`, `tonic-web`.** No drop-in
  replacements. Roll your own health endpoint via an Axum route or a plain
  proto-defined `HealthService`; reflection requires hand-rolling.
- **The `prost` ecosystem.** Code that hand-implements `prost::Message`,
  uses `prost-types`' well-known types directly, or depends on prost-reflect
  needs reworking. Buffa's view/owned split has no direct prost analogue.
- **`#[tonic::async_trait]` familiarity.** The plain `async fn` shape is
  cleaner but does require edition 2024.

## What you gain

- **One server, three protocols.** Connect, gRPC, gRPC-Web on the same
  endpoint — no separate setup for browser clients.
- **JSON encoding is built in.** `application/json` works on every RPC by
  default; curl-friendly sanity checks need no proto knowledge.
- **First-class Tower composition.** `tower-http`, `axum::middleware`, and
  any layer you write for axum routes also applies to RPC routes.
- **Zero-copy decode** for handlers that opt in (subject to the JSON-view
  incompatibility caveat).
- **Lower single-request latency** vs tonic 0.14: 1.35×–1.95× reported.

For day-two concerns (testing, observability), `testing.md` covers patterns
that work on both stacks — only the imports change.
