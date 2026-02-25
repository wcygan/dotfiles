# Async Error Handling

## The Double-Result Problem

`tokio::spawn` introduces a `JoinError` layer around your application error:

```rust
let handle = tokio::spawn(async {
    fallible_work().await  // Returns Result<T, AppError>
});
// handle.await is Result<Result<T, AppError>, JoinError>
```

### Flatten Helper

```rust
async fn spawn_flatten<T, E>(
    future: impl Future<Output = Result<T, E>> + Send + 'static,
) -> Result<T, anyhow::Error>
where
    T: Send + 'static,
    E: Into<anyhow::Error> + Send + 'static,
{
    tokio::spawn(future)
        .await
        .map_err(|je| {
            if je.is_panic() {
                tracing::error!("task panicked: {:?}", je);
                anyhow::anyhow!("spawned task panicked")
            } else {
                anyhow::anyhow!("task cancelled")
            }
        })?
        .map_err(Into::into)
}
```

### JoinSet Error Handling

```rust
let mut set = JoinSet::new();
set.spawn(work_a());
set.spawn(work_b());

while let Some(result) = set.join_next().await {
    match result {
        Ok(Ok(val)) => process(val),
        Ok(Err(e)) => tracing::warn!(?e, "task returned error"),
        Err(je) if je.is_panic() => tracing::error!("task panicked"),
        Err(je) => tracing::warn!("task cancelled: {je}"),
    }
}
```

## Error Crate Selection

| Crate | Use Case | Pattern |
|-------|----------|---------|
| `thiserror` | Libraries — precise, typed error enums | `#[derive(Error)]` with `#[from]` for conversions |
| `anyhow` | Applications — flexible error context | `anyhow::Result<T>` with `.context("description")` |
| `eyre` | Applications with custom formatting | User-facing CLIs needing pretty error output |

### Library Pattern (thiserror)

```rust
#[derive(Debug, thiserror::Error)]
pub enum ServiceError {
    #[error("database query failed: {0}")]
    Database(#[from] sqlx::Error),

    #[error("user {id} not found")]
    NotFound { id: u64 },

    #[error("request timeout after {0:?}")]
    Timeout(Duration),
}
```

### Application Pattern (anyhow)

```rust
use anyhow::{Context, Result};

async fn fetch_user(id: u64) -> Result<User> {
    let row = db.query_one("SELECT * FROM users WHERE id = $1", &[&id])
        .await
        .context("failed to query user")?;

    parse_user(row)
        .context("failed to parse user row")
}
```

**Key async-specific practice:** Always use `.context()` on async operations. Without it, error messages are too vague because the call stack is lost across await points.

## Panic Handling

### Set a Custom Panic Hook

```rust
std::panic::set_hook(Box::new(|info| {
    tracing::error!(panic = %info, "task panicked");
}));
```

### Use Named Tasks for Identification

```rust
tokio::task::Builder::new()
    .name("payment-processor")
    .spawn(async move { process_payments().await })?;
```

## gRPC Error Mapping (tonic)

```rust
impl From<ServiceError> for tonic::Status {
    fn from(err: ServiceError) -> Self {
        match err {
            ServiceError::NotFound { id } => {
                tonic::Status::not_found(format!("user {id} not found"))
            }
            ServiceError::Database(e) => {
                tracing::error!(?e, "database error");
                tonic::Status::internal("internal error")
            }
            ServiceError::Timeout(d) => {
                tonic::Status::deadline_exceeded(format!("timeout after {d:?}"))
            }
        }
    }
}
```

## HTTP Error Mapping (axum)

```rust
impl axum::response::IntoResponse for ServiceError {
    fn into_response(self) -> axum::response::Response {
        let (status, msg) = match &self {
            ServiceError::NotFound { .. } => (StatusCode::NOT_FOUND, self.to_string()),
            ServiceError::Database(_) => {
                tracing::error!(?self, "database error");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error".into())
            }
            ServiceError::Timeout(_) => (StatusCode::GATEWAY_TIMEOUT, self.to_string()),
        };
        (status, msg).into_response()
    }
}
```

## Key Documentation

- [anyhow docs](https://docs.rs/anyhow/latest/anyhow/)
- [thiserror docs](https://docs.rs/thiserror/latest/thiserror/)
- [Luca Palmieri: Error Handling in Rust](https://lpalmieri.com/posts/error-handling-rust/)
- [Tokio JoinError](https://docs.rs/tokio/latest/tokio/task/struct.JoinError.html)
