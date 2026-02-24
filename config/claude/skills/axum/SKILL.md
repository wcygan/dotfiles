---
name: axum
description: Axum Rust web framework expert. Auto-loads when working with axum Router, handlers, extractors, FromRequest, IntoResponse, State, middleware, tower layers, tower-http, axum::serve, method routing, Json extractor, Path extractor, Query extractor, error handling, or Rust HTTP APIs. Keywords: axum, router, handler, extractor, middleware, tower, IntoResponse, FromRequest, State, Rust web, HTTP API
---

# Axum

Axum is an ergonomic, modular Rust web framework built on Tokio, Hyper, and Tower. It uses extractors (no macros) for request parsing and Tower services/layers for middleware.

## Quick Start

```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(|| async { "Hello, World!" }));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## Core Architecture

- **Router** — maps paths to handlers/services; supports nesting, merging, fallbacks, layers
- **Handlers** — async fns taking extractors and returning `impl IntoResponse`
- **Extractors** — types implementing `FromRequest` / `FromRequestParts` that parse requests
- **Responses** — any type implementing `IntoResponse` (String, Json, StatusCode, tuples...)
- **Middleware** — Tower layers applied via `Router::layer()` or `middleware::from_fn`
- **State** — shared app state via `State<T>` extractor with `.with_state()`

## Handler Pattern

```rust
async fn create_user(
    State(db): State<Pool>,           // FromRequestParts (any position)
    Path(id): Path<u32>,              // FromRequestParts (any position)
    Json(payload): Json<CreateUser>,  // FromRequest (must be LAST)
) -> Result<Json<User>, StatusCode> {
    // ...
}
```

Rules: up to 16 args, all `FromRequestParts` except last which can be `FromRequest` (body).

## Common Extractors

| Extractor | Trait | Purpose |
|-----------|-------|---------|
| `Path<T>` | Parts | Deserialize path params |
| `Query<T>` | Parts | Deserialize query string |
| `State<T>` | Parts | Access shared app state |
| `HeaderMap` | Parts | All request headers |
| `Json<T>` | Request | Deserialize JSON body |
| `Form<T>` | Request | Deserialize form body |
| `String` / `Bytes` | Request | Raw body content |

## Routing

```rust
Router::new()
    .route("/users", get(list_users).post(create_user))
    .route("/users/{id}", get(get_user).put(update_user).delete(delete_user))
    .nest("/api", api_router)
    .merge(other_router)
    .fallback(handler_404)
    .layer(tower_http::trace::TraceLayer::new_for_http())
    .with_state(app_state)
```

## Error Pattern

```rust
enum AppError { NotFound, Internal(anyhow::Error) }

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        match self {
            AppError::NotFound => StatusCode::NOT_FOUND.into_response(),
            AppError::Internal(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
        }
    }
}

async fn handler() -> Result<Json<Data>, AppError> {
    let data = fetch().map_err(AppError::Internal)?;
    Ok(Json(data))
}
```

## Key Dependencies

```toml
[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
tower = "0.5"
tower-http = { version = "0.6", features = ["cors", "trace", "compression-gzip"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

## References

- [Routing](references/routing.md) — Router, method routing, path params, nesting, merging, fallback, layers
- [Handlers](references/handlers.md) — Handler trait, signatures, requirements, closures, debug_handler
- [Extractors](references/extractors.md) — all built-in extractors, ordering rules, optional, custom extractors
- [Responses](references/responses.md) — IntoResponse, IntoResponseParts, tuples, custom responses
- [State Management](references/state.md) — State extractor, Extension, closures, task-local patterns
- [Middleware](references/middleware.md) — from_fn, from_extractor, Tower layers, execution order
- [Error Handling](references/error-handling.md) — error model, Result pattern, rejections, HandleError
- [Tower-HTTP](references/tower-http.md) — CORS, tracing, compression, timeout, catch-panic, request-id
