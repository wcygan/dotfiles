---
title: State Management
description: Axum State extractor, Extension, closure captures, task-local patterns, and shared state best practices
tags: [axum, state, State, Extension, Arc, shared state]
---

# State Management

Axum offers four patterns for sharing state across handlers, ordered by preference.

## Pattern 1: State Extractor (Recommended)

Type-safe, compile-time checked, most idiomatic:

```rust
use axum::extract::State;

#[derive(Clone)]
struct AppState {
    db: DatabasePool,
    cache: RedisPool,
}

async fn handler(State(state): State<AppState>) -> impl IntoResponse {
    let users = state.db.query("SELECT * FROM users").await;
    Json(users)
}

let state = AppState { db: pool, cache: redis };
let app = Router::new()
    .route("/users", get(handler))
    .with_state(state);
```

### State Must Be Clone

State is cloned for each request. For large types, wrap in `Arc`:

```rust
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    inner: Arc<InnerState>,
}

struct InnerState {
    db: DatabasePool,
    config: Config,
}

let state = AppState {
    inner: Arc::new(InnerState { db: pool, config }),
};
```

### Substates

Extract only part of the state in a handler:

```rust
use axum::extract::FromRef;

#[derive(Clone)]
struct AppState {
    db: DatabasePool,
    api_key: String,
}

// Derive or implement FromRef for sub-parts
impl FromRef<AppState> for DatabasePool {
    fn from_ref(state: &AppState) -> Self {
        state.db.clone()
    }
}

// Handler only needs the pool, not the full state
async fn handler(State(db): State<DatabasePool>) -> impl IntoResponse {
    // ...
}
```

### Different State Per Router

```rust
let api_routes = Router::new()
    .route("/data", get(api_handler))
    .with_state(ApiState { ... });

let admin_routes = Router::new()
    .route("/dashboard", get(admin_handler))
    .with_state(AdminState { ... });

// Merge routers with different state types
let app = Router::new()
    .merge(api_routes)
    .merge(admin_routes);
```

## Pattern 2: Request Extensions

Dynamic, but types must match at runtime:

```rust
use axum::Extension;

#[derive(Clone)]
struct SharedData { value: String }

let app = Router::new()
    .route("/", get(handler))
    .layer(Extension(SharedData { value: "hello".into() }));

async fn handler(Extension(data): Extension<SharedData>) -> String {
    data.value
}
```

**Downsides**: runtime error (500) if Extension is missing. Prefer `State<T>` which is checked at compile time.

## Pattern 3: Closure Captures

Explicit but verbose:

```rust
let db = DatabasePool::connect("...").await;

let app = Router::new().route("/users", get({
    let db = db.clone();
    move || async move {
        let users = db.query("SELECT * FROM users").await;
        Json(users)
    }
}));
```

Use when state is only needed for one or two routes.

## Pattern 4: Task-Local Variables

Enables state access in `IntoResponse` implementations:

```rust
use tokio::task_local;

task_local! {
    pub static REQUEST_ID: String;
}

async fn handler() -> impl IntoResponse {
    // Set in middleware, accessible anywhere in the task
    let id = REQUEST_ID.with(|id| id.clone());
    format!("Request: {id}")
}
```

Niche pattern — use only when you need state in `IntoResponse` impls where you can't pass extractors.

## Common State Patterns

### Database Pool

```rust
#[derive(Clone)]
struct AppState {
    pool: sqlx::PgPool,
}

async fn list_users(State(state): State<AppState>) -> Result<Json<Vec<User>>, StatusCode> {
    let users = sqlx::query_as::<_, User>("SELECT * FROM users")
        .fetch_all(&state.pool)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    Ok(Json(users))
}
```

### Shared Mutable State

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

type SharedState = Arc<RwLock<HashMap<String, String>>>;

async fn get_value(
    State(state): State<SharedState>,
    Path(key): Path<String>,
) -> Result<String, StatusCode> {
    let store = state.read().await;
    store.get(&key).cloned().ok_or(StatusCode::NOT_FOUND)
}

async fn set_value(
    State(state): State<SharedState>,
    Path(key): Path<String>,
    body: String,
) -> StatusCode {
    state.write().await.insert(key, body);
    StatusCode::OK
}
```

### Configuration

```rust
#[derive(Clone)]
struct AppState {
    config: Arc<Config>,  // Arc since Config is large and read-only
    db: PgPool,
}

struct Config {
    jwt_secret: String,
    rate_limit: u32,
    cors_origins: Vec<String>,
}
```

## State and Middleware

Middleware applied with `from_fn_with_state` can access the same state:

```rust
let app = Router::new()
    .route("/protected", get(handler))
    .route_layer(middleware::from_fn_with_state(state.clone(), auth_middleware))
    .with_state(state);

async fn auth_middleware(
    State(state): State<AppState>,
    req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    // Validate auth using state.jwt_secret...
    Ok(next.run(req).await)
}
```
