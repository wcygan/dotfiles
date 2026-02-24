---
title: Testing
description: "#[sqlx::test] attribute macro, test database management, fixtures, function signatures, Pool/PoolConnection/PoolOptions parameters"
tags: [sqlx, test, testing, fixtures, database, isolation]
---

# Testing with SQLx

## #[sqlx::test] Attribute Macro

Requires the `migrate` feature. Provides automatic test database creation, migration, and cleanup.

## Basic Usage

```rust
#[sqlx::test]
async fn test_basic() {
    // Runs as a standard async test (like #[tokio::test])
    assert_eq!(1 + 1, 2);
}
```

## Function Signatures

### Pool Parameter

Receives a pool connected to a fresh test database:

```rust
#[sqlx::test]
async fn test_with_pool(pool: PgPool) -> sqlx::Result<()> {
    let count = sqlx::query_scalar!("SELECT COUNT(*) FROM users")
        .fetch_one(&pool)
        .await?;
    assert_eq!(count, Some(0));
    Ok(())
}
```

### PoolConnection Parameter

Receives a single connection:

```rust
#[sqlx::test]
async fn test_with_conn(mut conn: PgConnection) -> sqlx::Result<()> {
    sqlx::query!("INSERT INTO users (name) VALUES ($1)", "test")
        .execute(&mut conn)
        .await?;
    Ok(())
}
```

### PoolOptions + ConnectOptions (Advanced)

Custom pool configuration for the test:

```rust
#[sqlx::test]
async fn test_custom_pool(
    opts: PgPoolOptions,
    connect_opts: PgConnectOptions,
) -> sqlx::Result<()> {
    let pool = opts
        .max_connections(1)
        .connect_with(connect_opts)
        .await?;
    // use pool
    Ok(())
}
```

## Test Database Management

### How It Works

1. Each test gets a **unique database** (or file for SQLite)
2. Migrations from `./migrations/` are automatically applied
3. **Successful tests**: database is cleaned up
4. **Failed tests / panics**: database is preserved for debugging
5. **Next test run**: leftover test databases from previous runs are cleaned up

### Requirements

- **PostgreSQL/MySQL**: `DATABASE_URL` must be set (in env or `.env`)
- **SQLite**: No URL needed; uses `target/sqlx/test-dbs/<test_path>.sqlite`

### Database Naming

Test databases are named: `_sqlx_test_{test_binary}_{test_name}_{hash}`

## Migrations

### Default

Applies migrations from `./migrations/` automatically:

```rust
#[sqlx::test]  // migrations applied before test runs
async fn test_users_table(pool: PgPool) -> sqlx::Result<()> {
    // users table already exists
    Ok(())
}
```

### Custom Migration Path

```rust
#[sqlx::test(migrations = "tests/migrations")]
async fn test_with_custom_migrations(pool: PgPool) -> sqlx::Result<()> {
    Ok(())
}
```

### External Migrator

```rust
// Reference a Migrator from another crate
#[sqlx::test(migrator = "my_lib::MIGRATOR")]
async fn test_with_external_migrator(pool: PgPool) -> sqlx::Result<()> {
    Ok(())
}
```

### Disable Migrations

```rust
#[sqlx::test(migrations = false)]
async fn test_empty_database(pool: PgPool) -> sqlx::Result<()> {
    // no tables exist
    Ok(())
}
```

## Fixtures

SQL scripts for inserting test data, applied after migrations.

### Fixture File Location

Default: `./fixtures/` directory relative to the test file.

`fixtures/users.sql`:
```sql
INSERT INTO users (id, name, email) VALUES
    (1, 'Alice', 'alice@example.com'),
    (2, 'Bob', 'bob@example.com');
```

### Using Fixtures

```rust
// Simple: loads from ./fixtures/users.sql and ./fixtures/posts.sql
#[sqlx::test(fixtures("users", "posts"))]
async fn test_with_data(pool: PgPool) -> sqlx::Result<()> {
    let count = sqlx::query_scalar!("SELECT COUNT(*) FROM users")
        .fetch_one(&pool)
        .await?;
    assert_eq!(count, Some(2));
    Ok(())
}

// Full paths
#[sqlx::test(fixtures("./fixtures/users.sql"))]
async fn test_explicit_path(pool: PgPool) -> sqlx::Result<()> {
    Ok(())
}

// Path + scripts
#[sqlx::test(fixtures(path = "./test_data", scripts("users", "orders")))]
async fn test_custom_fixtures(pool: PgPool) -> sqlx::Result<()> {
    Ok(())
}
```

### Fixture Rules

- Applied in specified order — respect foreign key constraints
- Each fixture runs as a single command (implicit transaction)
- Multiple `fixtures()` attributes can be combined
- Fixtures are composable — keep them small and focused

## Test Organization

### Recommended Structure

```
tests/
├── common/
│   └── mod.rs          # shared helpers
├── fixtures/
│   ├── users.sql
│   ├── posts.sql
│   └── comments.sql
├── user_tests.rs
├── post_tests.rs
└── integration_tests.rs
```

### Shared Helpers

```rust
// tests/common/mod.rs
pub async fn create_test_user(pool: &PgPool, name: &str) -> i64 {
    sqlx::query_scalar!(
        "INSERT INTO users (name) VALUES ($1) RETURNING id", name
    )
    .fetch_one(pool)
    .await
    .unwrap()
}
```

## Testing Patterns

### Testing Transactions

```rust
#[sqlx::test]
async fn test_transaction_rollback(pool: PgPool) -> sqlx::Result<()> {
    let mut tx = pool.begin().await?;

    sqlx::query!("INSERT INTO users (name) VALUES ($1)", "temp")
        .execute(&mut *tx)
        .await?;

    tx.rollback().await?;

    let count = sqlx::query_scalar!("SELECT COUNT(*) FROM users")
        .fetch_one(&pool)
        .await?;
    assert_eq!(count, Some(0));

    Ok(())
}
```

### Testing Error Cases

```rust
#[sqlx::test(fixtures("users"))]
async fn test_duplicate_email_rejected(pool: PgPool) -> sqlx::Result<()> {
    let result = sqlx::query!(
        "INSERT INTO users (name, email) VALUES ($1, $2)",
        "Duplicate",
        "alice@example.com" // already exists from fixture
    )
    .execute(&pool)
    .await;

    assert!(result.is_err());
    if let Err(sqlx::Error::Database(db_err)) = result {
        assert!(db_err.is_unique_violation());
    }

    Ok(())
}
```

## Limitations

- Does not support `#[tokio::test]` control arguments (e.g., `flavor`, `worker_threads`)
- All test pools share a global connection limit to prevent exceeding server limits
- SQLite test databases are file-based, not in-memory
