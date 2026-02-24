---
title: Handlers
description: Axum handler trait, function signatures, requirements, closures, and debug_handler macro
tags: [axum, handler, async, function, debug_handler]
---

# Handlers

## What is a Handler?

A handler is an async function that takes zero or more extractors as arguments and returns something that implements `IntoResponse`.

```rust
// Zero extractors
async fn root() -> &'static str {
    "Hello, World!"
}

// One extractor
async fn echo(body: String) -> String {
    body
}

// Multiple extractors
async fn create_user(
    State(db): State<Pool>,
    Json(payload): Json<CreateUser>,
) -> Result<Json<User>, StatusCode> {
    // ...
}
```

## Handler Requirements

For an async fn to be a valid handler, it must satisfy:

1. **`async fn`** — must be async
2. **Up to 16 arguments** — all must implement `Send`
3. **All args except last** — must implement `FromRequestParts`
4. **Last argument** — may implement `FromRequest` (consumes body)
5. **Return type** — must implement `IntoResponse`
6. **Function itself** — must be `Clone + Send + 'static`
7. **Future** — must be `Send`

## Extractor Ordering

The ordering rule is critical:

```rust
// CORRECT: body extractor (Json) is LAST
async fn handler(
    method: Method,                   // FromRequestParts
    headers: HeaderMap,               // FromRequestParts
    State(state): State<AppState>,    // FromRequestParts
    Json(body): Json<Value>,          // FromRequest — LAST
) -> impl IntoResponse { ... }

// WRONG: body extractor not last — won't compile
async fn bad(
    Json(body): Json<Value>,          // FromRequest
    State(state): State<AppState>,    // after body — ERROR
) -> impl IntoResponse { ... }
```

## Closures as Handlers

Closures work if they implement `Clone + Send + 'static`:

```rust
let shared = Arc::new(data);

let app = Router::new().route("/", get({
    let shared = shared.clone();
    move || async move {
        format!("Data: {:?}", shared)
    }
}));
```

This pattern is mostly superseded by `State<T>` but useful in niche cases.

## Handler Composition

### Adding Layers to Handlers

```rust
use tower::limit::ConcurrencyLimitLayer;

let app = Router::new().route(
    "/",
    get(handler.layer(ConcurrencyLimitLayer::new(10))),
);
```

### with_state on Handlers

```rust
let app = Router::new().route(
    "/",
    get(handler).with_state(my_state),
);
```

## debug_handler Macro

When handler trait bounds fail, Rust gives cryptic errors. Use `#[debug_handler]` for clear messages:

```rust
use axum::debug_handler;

#[debug_handler]
async fn handler(
    Json(body): Json<Value>,
    State(state): State<AppState>,  // Oops — after body
) -> impl IntoResponse {
    // Compiler gives a clear error about extractor ordering
}
```

Enable with `axum-macros` feature:

```toml
[dependencies]
axum = { version = "0.8", features = ["macros"] }
```

Always use `#[debug_handler]` during development. Remove in production if desired.

## debug_middleware Macro

Similarly helps debug middleware function signatures:

```rust
use axum::debug_middleware;

#[debug_middleware]
async fn my_middleware(req: Request, next: Next) -> Response {
    next.run(req).await
}
```

## Handler as Service

Convert a handler into a Tower `Service` with `HandlerService`:

```rust
use axum::handler::HandlerWithoutStateExt;

// Useful when you need to pass a handler where a Service is expected
let svc = handler.into_service();
```

## Returning Different Response Types

Use `impl IntoResponse` or a concrete `Response`:

```rust
use axum::response::{IntoResponse, Response};

async fn handler(id: Path<u32>) -> Response {
    if *id == 0 {
        return StatusCode::BAD_REQUEST.into_response();
    }
    Json(get_user(*id)).into_response()
}
```

Or use `Result`:

```rust
async fn handler() -> Result<Json<Data>, StatusCode> {
    let data = fetch().map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    Ok(Json(data))
}
```
