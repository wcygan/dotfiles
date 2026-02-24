---
title: Routing
description: Axum Router, method routing, path parameters, wildcards, nesting, merging, fallback, and route layers
tags: [axum, routing, router, path, nest, merge, fallback]
---

# Routing

## Router

The `Router` is axum's central type for composing handlers and services.

```rust
use axum::{routing::{get, post, put, delete}, Router};

let app = Router::new()
    .route("/", get(root))
    .route("/users", get(list_users).post(create_user))
    .route("/users/{id}", get(get_user).put(update_user).delete(delete_user));
```

## Method Routing Functions

Each HTTP method has a dedicated routing function:

| Function | HTTP Method |
|----------|-------------|
| `get(handler)` | GET |
| `post(handler)` | POST |
| `put(handler)` | PUT |
| `delete(handler)` | DELETE |
| `patch(handler)` | PATCH |
| `head(handler)` | HEAD |
| `options(handler)` | OPTIONS |
| `trace(handler)` | TRACE |
| `any(handler)` | Any method |
| `on(MethodFilter, handler)` | Custom filter |

Chain methods on a `MethodRouter`:

```rust
use axum::routing::{get, post, MethodRouter};

// Multiple methods on the same path
.route("/items", get(list).post(create).delete(delete_all))
```

## Path Parameters

Use `{name}` syntax in route paths. Extract with `Path<T>`:

```rust
use axum::extract::Path;

// Single parameter
.route("/users/{id}", get(get_user))

async fn get_user(Path(id): Path<u32>) -> String {
    format!("User {id}")
}

// Multiple parameters — use tuple
.route("/users/{user_id}/posts/{post_id}", get(get_post))

async fn get_post(Path((user_id, post_id)): Path<(u32, u32)>) -> String {
    format!("User {user_id}, Post {post_id}")
}

// Named parameters with struct
#[derive(Deserialize)]
struct PostParams { user_id: u32, post_id: u32 }

async fn get_post_named(Path(params): Path<PostParams>) -> String {
    format!("User {}, Post {}", params.user_id, params.post_id)
}
```

## Wildcards

Capture remaining path segments with `{*name}`:

```rust
.route("/files/{*path}", get(serve_file))

async fn serve_file(Path(path): Path<String>) -> String {
    // path = "docs/readme.md" for /files/docs/readme.md
    format!("Serving: {path}")
}
```

## Nesting Routers

`nest` strips the prefix and delegates to a sub-router:

```rust
let api = Router::new()
    .route("/users", get(list_users))    // matches /api/users
    .route("/posts", get(list_posts));   // matches /api/posts

let app = Router::new()
    .nest("/api", api);
```

Nesting rules:
- The prefix is stripped before the nested router sees the request
- Nested routers can have their own state (via `.with_state()`)
- Use `OriginalUri` extractor to get the full original URI in nested handlers

## Merging Routers

`merge` combines routes from two routers:

```rust
let user_routes = Router::new()
    .route("/users", get(list_users));

let post_routes = Router::new()
    .route("/posts", get(list_posts));

let app = user_routes.merge(post_routes);
```

Merge panics at startup if routes overlap (same path + method).

## Fallback Handler

Handle unmatched routes:

```rust
let app = Router::new()
    .route("/", get(root))
    .fallback(handler_404);

async fn handler_404() -> (StatusCode, &'static str) {
    (StatusCode::NOT_FOUND, "Nothing here")
}
```

Fallback behavior with nesting:
- Each nested router can have its own fallback
- If a nested router has no fallback, unmatched requests fall through to the parent

## Layers on Routes

Apply middleware to specific routes or the entire router:

```rust
use tower_http::trace::TraceLayer;
use axum::middleware;

let app = Router::new()
    // Layer on specific routes
    .route("/api/users", get(list_users))
    .route_layer(middleware::from_fn(require_auth))
    // Layer on entire router (including fallback)
    .layer(TraceLayer::new_for_http());
```

**`layer` vs `route_layer`:**
- `layer(L)` — applies to all routes AND the fallback
- `route_layer(L)` — applies to matched routes only, NOT the fallback

## Service Routes

Mount arbitrary Tower services:

```rust
use tower::service_fn;

let app = Router::new()
    .route_service("/static", tower_http::services::ServeDir::new("assets"));
```

## Route Ordering

Routes are matched by specificity, not insertion order. More specific paths take priority:

```rust
Router::new()
    .route("/users/me", get(current_user))     // matches /users/me
    .route("/users/{id}", get(get_user))        // matches /users/123
```

## State with Router

```rust
let app = Router::new()
    .route("/", get(handler))
    .with_state(AppState { db: pool });

// Must be called LAST — consumes the router
// State type must match what handlers expect
```
