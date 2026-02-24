---
title: Error Handling
description: SQLx Error enum variants, DatabaseError trait, matching specific errors, common error patterns and recovery strategies
tags: [sqlx, error, database error, error handling, matching]
---

# Error Handling

## The Error Enum

`sqlx::Error` is non-exhaustive. Key variants:

### Configuration & Arguments

| Variant | Cause |
|---------|-------|
| `Configuration` | Invalid connection string or config |
| `InvalidArgument(String)` | Invalid function parameter |

### Database Operations

| Variant | Cause |
|---------|-------|
| `Database(Box<dyn DatabaseError>)` | Error returned by the database server |
| `RowNotFound` | `fetch_one()` returned zero rows |
| `TypeNotFound` | Referenced type doesn't exist in database |

### Data Encoding/Decoding

| Variant | Cause |
|---------|-------|
| `Encode(Box<dyn Error>)` | Failed to encode value for database |
| `Decode(Box<dyn Error>)` | Failed to decode value from database |
| `ColumnDecode { index, source }` | Decode error for a specific column |
| `ColumnNotFound(String)` | Named column doesn't exist in result |
| `ColumnIndexOutOfBounds { index, len }` | Column index exceeds result set |

### Connection

| Variant | Cause |
|---------|-------|
| `Io(io::Error)` | Network/IO error |
| `Tls(Box<dyn Error>)` | TLS handshake failure |
| `Protocol(String)` | Unexpected data in protocol |

### Pool

| Variant | Cause |
|---------|-------|
| `PoolTimedOut` | `acquire_timeout` exceeded |
| `PoolClosed` | Pool was closed during acquire |
| `WorkerCrashed` | Background pool worker panicked |

### Other

| Variant | Cause |
|---------|-------|
| `Migrate(Box<MigrateError>)` | Migration failure (requires `migrate` feature) |

## Matching Database Errors

The `Database` variant wraps a `dyn DatabaseError` trait object with rich methods:

```rust
match result {
    Ok(row) => { /* success */ }
    Err(sqlx::Error::Database(db_err)) => {
        // Common DatabaseError methods:
        println!("Message: {}", db_err.message());
        println!("Code: {:?}", db_err.code());        // e.g., Some("23505")
        println!("Constraint: {:?}", db_err.constraint()); // e.g., Some("users_email_key")
        println!("Table: {:?}", db_err.table());

        // Convenience checks
        if db_err.is_unique_violation() {
            // handle duplicate
        } else if db_err.is_foreign_key_violation() {
            // handle FK constraint
        } else if db_err.is_check_violation() {
            // handle check constraint
        }
    }
    Err(e) => { /* other error */ }
}
```

## DatabaseError Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `message()` | `&str` | Human-readable error message |
| `code()` | `Option<Cow<str>>` | Database-specific error code |
| `constraint()` | `Option<&str>` | Constraint that caused the error |
| `table()` | `Option<&str>` | Table involved |
| `kind()` | `ErrorKind` | Categorized error kind |
| `is_unique_violation()` | `bool` | Duplicate key error |
| `is_foreign_key_violation()` | `bool` | FK constraint failed |
| `is_check_violation()` | `bool` | CHECK constraint failed |

## Extracting DatabaseError

```rust
// Borrow (doesn't consume)
if let Some(db_err) = error.as_database_error() {
    println!("{}", db_err.message());
}

// Consume (takes ownership)
if let Some(db_err) = error.into_database_error() {
    // db_err: Box<dyn DatabaseError>
}
```

## Common Error Patterns

### Unique Constraint Violation

```rust
async fn create_user(pool: &PgPool, email: &str) -> Result<User, AppError> {
    sqlx::query_as!(User, "INSERT INTO users (email) VALUES ($1) RETURNING *", email)
        .fetch_one(pool)
        .await
        .map_err(|e| match e {
            sqlx::Error::Database(ref db_err) if db_err.is_unique_violation() => {
                AppError::Conflict(format!("Email {} already exists", email))
            }
            _ => AppError::Internal(e.into()),
        })
}
```

### Row Not Found → 404

```rust
async fn get_user(pool: &PgPool, id: i64) -> Result<User, AppError> {
    sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(pool)
        .await
        .map_err(|e| match e {
            sqlx::Error::RowNotFound => AppError::NotFound(format!("User {} not found", id)),
            _ => AppError::Internal(e.into()),
        })
}

// Alternative: use fetch_optional and handle None
async fn get_user_opt(pool: &PgPool, id: i64) -> Result<Option<User>, sqlx::Error> {
    sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(pool)
        .await
}
```

### Pool Timeout → Retry or Backpressure

```rust
match pool.acquire().await {
    Ok(conn) => { /* use connection */ }
    Err(sqlx::Error::PoolTimedOut) => {
        // Database is under load; apply backpressure
        return Err(AppError::ServiceUnavailable("Database busy"));
    }
    Err(e) => return Err(e.into()),
}
```

### Serialization Failure → Retry

```rust
async fn transfer_funds(pool: &PgPool, from: i64, to: i64, amount: f64) -> Result<()> {
    for attempt in 0..3 {
        let mut tx = pool.begin_with("BEGIN ISOLATION LEVEL SERIALIZABLE").await?;

        let result = execute_transfer(&mut tx, from, to, amount).await;

        match result {
            Ok(_) => {
                tx.commit().await?;
                return Ok(());
            }
            Err(sqlx::Error::Database(ref db_err))
                if db_err.code().as_deref() == Some("40001") =>
            {
                // Serialization failure — retry
                eprintln!("Serialization conflict, attempt {}", attempt + 1);
                continue;
            }
            Err(e) => return Err(e.into()),
        }
    }
    Err(anyhow!("Max retries exceeded"))
}
```

## PostgreSQL Error Codes

Common codes you might match on:

| Code | Name | Constant |
|------|------|----------|
| 23505 | unique_violation | `is_unique_violation()` |
| 23503 | foreign_key_violation | `is_foreign_key_violation()` |
| 23514 | check_violation | `is_check_violation()` |
| 40001 | serialization_failure | Manual code check |
| 40P01 | deadlock_detected | Manual code check |
| 57014 | query_canceled | Manual code check |
| 42P01 | undefined_table | Manual code check |

## Wrapping in Application Errors

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),
    #[error("Conflict: {0}")]
    Conflict(String),
    #[error("Service unavailable: {0}")]
    ServiceUnavailable(&'static str),
    #[error("Internal error")]
    Internal(#[from] anyhow::Error),
}

impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        match &err {
            sqlx::Error::RowNotFound => AppError::NotFound("Resource not found".into()),
            sqlx::Error::Database(db_err) if db_err.is_unique_violation() => {
                AppError::Conflict("Duplicate entry".into())
            }
            sqlx::Error::PoolTimedOut => AppError::ServiceUnavailable("Database busy"),
            _ => AppError::Internal(err.into()),
        }
    }
}
```
