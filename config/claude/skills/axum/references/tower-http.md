---
title: Tower-HTTP Middleware
description: Common tower-http middleware used with axum including CORS, tracing, compression, timeout, catch-panic, request-id, and more
tags: [axum, tower-http, CORS, tracing, compression, timeout, middleware]
---

# Tower-HTTP Middleware

`tower-http` provides production-ready HTTP middleware. Enable features individually in Cargo.toml.

## Cargo.toml Setup

```toml
[dependencies]
tower-http = { version = "0.6", features = [
    "cors",
    "trace",
    "compression-gzip",
    "timeout",
    "catch-panic",
    "request-id",
    "sensitive-headers",
    "set-header",
    "limit",
    "normalize-path",
] }
tower = "0.5"
```

## TraceLayer — Request/Response Logging

```rust
use tower_http::trace::TraceLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(TraceLayer::new_for_http());
```

Custom tracing:

```rust
use tower_http::trace::{TraceLayer, DefaultMakeSpan, DefaultOnResponse};
use tracing::Level;

let app = Router::new()
    .route("/", get(handler))
    .layer(
        TraceLayer::new_for_http()
            .make_span_with(DefaultMakeSpan::new().level(Level::INFO))
            .on_response(DefaultOnResponse::new().level(Level::INFO))
    );
```

## CorsLayer — Cross-Origin Resource Sharing

```rust
use tower_http::cors::{CorsLayer, Any};
use http::Method;

// Permissive (development)
let cors = CorsLayer::permissive();

// Restrictive (production)
let cors = CorsLayer::new()
    .allow_origin("https://example.com".parse::<HeaderValue>().unwrap())
    .allow_methods([Method::GET, Method::POST, Method::PUT, Method::DELETE])
    .allow_headers([header::CONTENT_TYPE, header::AUTHORIZATION])
    .max_age(Duration::from_secs(3600));

// Multiple origins
let cors = CorsLayer::new()
    .allow_origin([
        "https://example.com".parse::<HeaderValue>().unwrap(),
        "https://app.example.com".parse::<HeaderValue>().unwrap(),
    ]);

let app = Router::new()
    .route("/api/data", get(handler))
    .layer(cors);
```

## CompressionLayer — Response Compression

```rust
use tower_http::compression::CompressionLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(CompressionLayer::new());
// Supports gzip, deflate, br, zstd based on Accept-Encoding
```

Selective compression:

```rust
let compression = CompressionLayer::new()
    .gzip(true)
    .br(true)
    .zstd(false)
    .deflate(false);
```

## TimeoutLayer — Request Timeouts

```rust
use tower_http::timeout::TimeoutLayer;
use tower::ServiceBuilder;
use axum::error_handling::HandleErrorLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(HandleErrorLayer::new(|_: BoxError| async {
                StatusCode::REQUEST_TIMEOUT
            }))
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
    );
```

**Important**: `TimeoutLayer` produces errors, so always pair with `HandleErrorLayer`.

## CatchPanicLayer — Panic Recovery

```rust
use tower_http::catch_panic::CatchPanicLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(CatchPanicLayer::new());
// Converts panics to 500 responses instead of crashing the server
```

Custom panic response:

```rust
use tower_http::catch_panic::CatchPanicLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(CatchPanicLayer::custom(|_err| {
        Response::builder()
            .status(StatusCode::INTERNAL_SERVER_ERROR)
            .body(Body::from("Internal Server Error"))
            .unwrap()
    }));
```

## RequestIdLayer — Request Tracking

```rust
use tower_http::request_id::{
    MakeRequestId, RequestId, SetRequestIdLayer, PropagateRequestIdLayer,
};

#[derive(Clone)]
struct MyMakeRequestId;

impl MakeRequestId for MyMakeRequestId {
    fn make_request_id<B>(&mut self, _req: &Request<B>) -> Option<RequestId> {
        Some(RequestId::new(uuid::Uuid::new_v4().to_string().parse().unwrap()))
    }
}

let app = Router::new()
    .route("/", get(handler))
    .layer(SetRequestIdLayer::x_request_id(MyMakeRequestId))
    .layer(PropagateRequestIdLayer::x_request_id());
```

## RequestBodyLimitLayer — Body Size Limits

```rust
use tower_http::limit::RequestBodyLimitLayer;

let app = Router::new()
    .route("/upload", post(upload_handler))
    .layer(RequestBodyLimitLayer::new(10 * 1024 * 1024)); // 10MB
```

Or per-route with axum's `DefaultBodyLimit`:

```rust
use axum::extract::DefaultBodyLimit;

let app = Router::new()
    .route("/upload", post(upload_handler))
    .route_layer(DefaultBodyLimit::max(50 * 1024 * 1024))  // 50MB for this route
    .route("/api", post(api_handler));  // default 2MB
```

## SensitiveHeadersLayer — Redact Headers in Logs

```rust
use tower_http::sensitive_headers::SetSensitiveHeadersLayer;
use http::header;

let app = Router::new()
    .route("/", get(handler))
    .layer(SetSensitiveHeadersLayer::new([
        header::AUTHORIZATION,
        header::COOKIE,
        header::SET_COOKIE,
    ]));
// Headers marked sensitive won't appear in tracing output
```

## SetResponseHeaderLayer — Add Headers

```rust
use tower_http::set_header::SetResponseHeaderLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(SetResponseHeaderLayer::overriding(
        header::SERVER,
        HeaderValue::from_static("my-app"),
    ));
```

## NormalizePathLayer — Clean Up Paths

```rust
use tower_http::normalize_path::NormalizePathLayer;

// Must wrap the entire router (before routing happens)
let app = NormalizePathLayer::trim_trailing_slash()
    .layer(Router::new()
        .route("/foo", get(handler))  // matches /foo and /foo/
    );
```

**Important**: `NormalizePathLayer` must be the outermost layer (applied before routing), so use `tower::ServiceExt::layer` not `Router::layer`.

## Full Production Stack

```rust
use tower::ServiceBuilder;
use tower_http::{
    cors::CorsLayer,
    trace::TraceLayer,
    compression::CompressionLayer,
    timeout::TimeoutLayer,
    catch_panic::CatchPanicLayer,
    request_id::{SetRequestIdLayer, PropagateRequestIdLayer},
    sensitive_headers::SetSensitiveHeadersLayer,
};

let app = Router::new()
    .route("/api/data", get(handler))
    .layer(
        ServiceBuilder::new()
            // Outermost — runs first on request
            .layer(SetSensitiveHeadersLayer::new([header::AUTHORIZATION]))
            .layer(SetRequestIdLayer::x_request_id(MyMakeRequestId))
            .layer(PropagateRequestIdLayer::x_request_id())
            .layer(TraceLayer::new_for_http())
            .layer(CatchPanicLayer::new())
            .layer(HandleErrorLayer::new(|_: BoxError| async {
                StatusCode::REQUEST_TIMEOUT
            }))
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(CorsLayer::permissive())
            .layer(CompressionLayer::new())
            // Innermost — runs last on request, first on response
    )
    .with_state(state);
```

## Serving Static Files

```rust
use tower_http::services::{ServeDir, ServeFile};

let app = Router::new()
    .route("/api/data", get(handler))
    .nest_service("/static", ServeDir::new("assets"))
    .fallback_service(ServeFile::new("assets/index.html"));
```

With cache headers:

```rust
use tower_http::services::ServeDir;
use tower_http::set_header::SetResponseHeaderLayer;

let serve_dir = ServeDir::new("assets")
    .append_index_html_on_directories(true);

let app = Router::new()
    .nest_service("/static", serve_dir);
```
