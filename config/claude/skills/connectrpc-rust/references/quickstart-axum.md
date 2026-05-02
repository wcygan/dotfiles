# Quickstart: ConnectRPC + Axum

The preferred path for any new project. Two crates, one `build.rs`, one `main.rs`.

## Table of contents

- [Layout](#layout)
- [Cargo.toml](#cargotoml)
- [proto/greet.proto](#protogreetproto)
- [build.rs](#buildrs)
- [src/main.rs](#srcmainrs)
- [Run and exercise](#run-and-exercise)
- [What to read next](#what-to-read-next)

## Layout

```
my-service/
├── Cargo.toml
├── build.rs
├── proto/
│   └── greet.proto
└── src/
    └── main.rs
```

## Cargo.toml

```toml
[package]
name = "my-service"
version = "0.1.0"
edition = "2024"
rust-version = "1.88"

[dependencies]
connectrpc = { version = "0.3", features = ["axum"] }
axum = "0.7"
tokio = { version = "1", features = ["macros", "rt-multi-thread", "net", "signal"] }

[build-dependencies]
connectrpc-build = "0.3"
```

Add `client` / `client-tls` only if this binary will also act as a ConnectRPC
*client*. Add `server-tls` only if you are terminating TLS in-process; reverse
proxies (Envoy, ALB) usually obviate that.

## proto/greet.proto

```proto
syntax = "proto3";
package greet.v1;

service GreetService {
  rpc Greet(GreetRequest) returns (GreetResponse);
}

message GreetRequest { string name = 1; }
message GreetResponse { string greeting = 1; }
```

## build.rs

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

`include_file` collects all generated modules into one file you can pull into
`main.rs` with `include!(concat!(env!("OUT_DIR"), "/_connectrpc.rs"));`.

## src/main.rs

```rust
use std::sync::Arc;

use axum::Router;
use connectrpc::{Response, RequestContext, ServiceResult, OwnedView};

include!(concat!(env!("OUT_DIR"), "/_connectrpc.rs"));

use greet::v1::{GreetService, GreetRequestView, GreetResponse};

struct MyGreet;

impl GreetService for MyGreet {
    async fn greet(
        &self,
        _ctx: RequestContext,
        req: OwnedView<GreetRequestView<'static>>,
    ) -> ServiceResult<GreetResponse> {
        Response::ok(GreetResponse {
            greeting: format!("Hello, {}!", req.name),
            ..Default::default()
        })
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let service = Arc::new(MyGreet);
    let connect_router = service.register(Router::new());
    let app: Router = connect_router.into_axum_router();

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    axum::serve(listener, app)
        .with_graceful_shutdown(async {
            tokio::signal::ctrl_c().await.ok();
        })
        .await?;
    Ok(())
}
```

Why this shape:

- `Arc<MyGreet>` so handlers can be `Sync` and shared across tasks. The
  generated `register` extension takes anything that implements the service
  trait and is `Send + Sync + 'static`.
- `into_axum_router()` returns an `axum::Router` you can `.layer(...)`,
  `.merge(...)`, or `.fallback_service(...)` like any other router.
- `axum::serve` (not `connectrpc::Server`) so observability and graceful
  shutdown match the rest of your service.

## Run and exercise

```bash
cargo run

# Connect (binary):
curl -sS http://localhost:8080/greet.v1.GreetService/Greet \
  -H 'content-type: application/proto' \
  --data-binary @<(printf '\x0a\x05world')

# Connect (JSON — easiest for sanity checks):
curl -sS http://localhost:8080/greet.v1.GreetService/Greet \
  -H 'content-type: application/json' \
  -d '{"name":"world"}'
```

The same handler also serves gRPC (HTTP/2) and gRPC-Web on the same path —
clients pick the protocol via headers.

## What to read next

- Adding handlers, response headers/trailers, streaming → `server.md`
- Building a Rust client for this service → `client.md`
- Wiring auth / tracing / timeouts via Axum and Tower → `server.md` middleware section
- Why JSON requests behave differently when handlers return views → `gotchas.md`
