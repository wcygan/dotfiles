# Client: HttpClient, ClientConfig, CallOptions, response patterns

Enable the `client` feature (or `client-tls` for TLS):

```toml
connectrpc = { version = "0.4", features = ["client", "client-tls"] }
```

## Table of contents

- [HttpClient](#httpclient)
- [ClientConfig](#clientconfig)
- [Generated client trait](#generated-client-trait)
- [CallOptions](#calloptions)
- [Response access patterns](#response-access-patterns)
- [Streaming clients](#streaming-clients)
- [Errors on the client side](#errors-on-the-client-side)

## HttpClient

```rust
use connectrpc::client::HttpClient;

// Cleartext only
let http = HttpClient::plaintext();

// TLS — pass an Arc<rustls::ClientConfig>
let mut tls = rustls::ClientConfig::builder()
    .with_root_certificates(roots())
    .with_no_client_auth();
let http = HttpClient::with_tls(std::sync::Arc::new(tls));
```

Reuse one `HttpClient` across the whole process — it owns the connection pool.
Cloning is cheap (`Arc` inside).

## ClientConfig

```rust
use std::time::Duration;
use connectrpc::client::ClientConfig;

let config = ClientConfig::new("https://api.example.com".parse()?)
    .default_timeout(Duration::from_secs(30))
    .default_header("authorization", "Bearer …");
```

`default_timeout` and `default_header` apply to every call; per-call
`CallOptions` override them.

## Generated client trait

`connectrpc-build` emits a `GreetServiceClient` (one per service). Construct it
from `(http_client, client_config)`:

```rust
use greet::v1::GreetServiceClient;

let client = GreetServiceClient::new(http.clone(), config);

let resp = client.greet(GreetRequest { name: "world".into(), ..Default::default() }).await?;
println!("{}", resp.view().greeting);
```

The generated trait has both `greet(req)` (uses defaults) and
`greet_with_options(req, opts)` for per-call control.

## CallOptions

```rust
use connectrpc::client::CallOptions;

let opts = CallOptions::default()
    .with_timeout(Duration::from_secs(5))
    .with_max_message_size(1024 * 1024)
    .with_header("x-request-id", req_id);

let resp = client.greet_with_options(req, opts).await?;
```

Per-call options *replace* defaults for that call only — inherited headers
from `ClientConfig::default_header` still apply unless explicitly overridden.

## Response access patterns

The same response value supports three access shapes — pick one per call site:

```rust
// 1. Borrow the view (zero-copy, scoped to `resp`):
let greeting: &str = resp.view().greeting;

// 2. Consume into an OwnedView (still borrowed from internal buffer,
//    but moves the buffer ownership into the view):
let view = resp.into_view();

// 3. Convert to a fully-owned proto struct:
let owned: GreetResponse = resp.into_owned();
```

Reach for `into_owned()` only when you need to outlive the response (e.g.
storing in a cache, returning across an `async` boundary that drops the buffer).

## Streaming clients

Server-streaming returns a `ServiceStream<RespMsg>`:

```rust
use futures::StreamExt;

let mut stream = client.range(RangeRequest { start: 0, end: 10, ..Default::default() }).await?;
while let Some(item) = stream.next().await {
    let resp = item?;
    println!("{}", resp.view().value);
}
```

Bidirectional and client-streaming clients accept a `ServiceStream<ReqMsg>`
input — typically built with `tokio::sync::mpsc` for fan-in or
`futures::stream::iter` for one-shot.

## Errors on the client side

Errors come back as `ConnectError` regardless of which protocol the transport
chose. Pattern-match on `error.code()`:

```rust
use connectrpc::{ConnectError, ErrorCode};

match client.greet(req).await {
    Ok(resp) => { /* … */ }
    Err(e) if e.code() == ErrorCode::Unauthenticated => prompt_login(),
    Err(e) if e.code() == ErrorCode::DeadlineExceeded => /* retry budget */,
    Err(e) => return Err(e.into()),
}
```

`ErrorDetail` entries on the server propagate through to the client; pull them
back out via `e.details()` to drive structured handling. See `errors.md`.
