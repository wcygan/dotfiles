---
title: Connection Pooling
description: Pool creation, PoolOptions configuration, connection lifecycle, Executor impl, graceful shutdown
tags: [sqlx, pool, connection, pooloptions, lifecycle, executor]
---

# Connection Pooling

## Why Pool

Connection pools solve three problems:
1. **Connection overhead**: Establishing new connections is expensive (TCP + auth + TLS)
2. **Server limits**: Databases typically cap at 100-150 connections
3. **Query plan caching**: Reused connections retain cached query plans

## Creating a Pool

### Direct Connect (Eager)

```rust
use sqlx::postgres::PgPoolOptions;

let pool = PgPoolOptions::new()
    .max_connections(5)
    .connect("postgres://user:pass@localhost/db")
    .await?;
```

### Lazy Connect

```rust
// No connections established until first use
let pool = PgPoolOptions::new()
    .max_connections(5)
    .connect_lazy("postgres://user:pass@localhost/db")?;
```

### From ConnectOptions

```rust
use sqlx::postgres::PgConnectOptions;

let options = PgConnectOptions::new()
    .host("localhost")
    .port(5432)
    .database("mydb")
    .username("user")
    .password("pass")
    .ssl_mode(PgSslMode::Require);

let pool = PgPoolOptions::new()
    .max_connections(10)
    .connect_with(options)
    .await?;
```

## PoolOptions Configuration

```rust
use std::time::Duration;

let pool = PgPoolOptions::new()
    .max_connections(10)          // Max active connections (default: 10)
    .min_connections(2)           // Pre-created idle connections (default: 0)
    .acquire_timeout(Duration::from_secs(30))  // Wait for available connection
    .idle_timeout(Duration::from_secs(600))    // Close idle connections after 10min
    .max_lifetime(Duration::from_secs(1800))   // Max connection age (30min)
    .test_before_acquire(true)    // Validate connection before checkout (default: true)
    .connect("postgres://...")
    .await?;
```

### Recommended Settings by Workload

| Setting | Web API | Background Worker | CLI Tool |
|---------|---------|-------------------|----------|
| `max_connections` | 10-20 | 2-5 | 1-2 |
| `min_connections` | 2-5 | 1 | 0 |
| `acquire_timeout` | 5-10s | 30s | 60s |
| `idle_timeout` | 10min | 5min | 30s |
| `max_lifetime` | 30min | 30min | None |

## Acquiring Connections

```rust
// Blocking wait (respects acquire_timeout)
let conn = pool.acquire().await?;

// Non-blocking attempt
if let Some(conn) = pool.try_acquire() {
    // use connection
}
```

Connections are returned to the pool when the `PoolConnection` is dropped.

## Pool as Executor

Pool implements `Executor`, so you can pass `&pool` directly to queries:

```rust
// No explicit acquire needed
let users = sqlx::query_as!(User, "SELECT * FROM users")
    .fetch_all(&pool)
    .await?;
```

Internally, this acquires a connection, executes the query, and returns the connection to the pool.

## Clone Behavior

```rust
let pool2 = pool.clone(); // Cheap: reference-counted handle
// Both point to the same underlying connection pool
```

Use this to share the pool across tasks, handlers, and middleware.

## Pool Status

```rust
pool.size()       // Current number of connections (idle + in-use)
pool.num_idle()   // Connections available for checkout
pool.is_closed()  // Whether close() has been called
```

## Graceful Shutdown

```rust
// Prevents new acquisitions, waits for in-use connections to return
pool.close().await;

// Or listen for the close event
let event = pool.close_event();
tokio::spawn(async move {
    event.await;
    println!("Pool closed");
});
```

Always call `.close().await` for client/server databases (Postgres, MySQL) to notify the server. SQLite connections are local and can just be dropped.

## Type Aliases

| Alias | Full Type |
|-------|-----------|
| `PgPool` | `Pool<Postgres>` |
| `MySqlPool` | `Pool<MySql>` |
| `SqlitePool` | `Pool<Sqlite>` |

## Common Patterns

### Axum State

```rust
use axum::{extract::State, Router};

async fn get_users(State(pool): State<PgPool>) -> impl IntoResponse {
    let users = sqlx::query_as!(User, "SELECT * FROM users")
        .fetch_all(&pool)
        .await
        .unwrap();
    Json(users)
}

let app = Router::new()
    .route("/users", get::get(get_users))
    .with_state(pool);
```

### Actix-web Data

```rust
use actix_web::web;

async fn get_users(pool: web::Data<PgPool>) -> impl Responder {
    let users = sqlx::query_as!(User, "SELECT * FROM users")
        .fetch_all(pool.get_ref())
        .await
        .unwrap();
    HttpResponse::Ok().json(users)
}
```

## Common Pitfalls

- **Too many connections**: Match `max_connections` to your database's limit divided by app instances
- **No acquire timeout**: Default is 30s; set shorter for web APIs to fail fast
- **Forgetting close()**: Connections may linger on the server after process exit
- **Pool per request**: Never create a new pool per request; create once and share
