---
title: Transactions
description: Transaction lifecycle, commit/rollback, auto-rollback on drop, savepoints, isolation levels, passing transactions to functions
tags: [sqlx, transaction, commit, rollback, savepoint, isolation]
---

# Transactions

## Starting a Transaction

### From Pool

```rust
let mut tx = pool.begin().await?;
```

### From Connection

```rust
let mut conn = pool.acquire().await?;
let mut tx = conn.begin().await?;
```

### Custom BEGIN Statement

```rust
// PostgreSQL isolation levels
let mut tx = pool.begin_with("BEGIN ISOLATION LEVEL SERIALIZABLE").await?;
```

### Non-Blocking

```rust
if let Some(mut tx) = pool.try_begin().await? {
    // use transaction
}
```

## Executing Queries in a Transaction

Pass `&mut *tx` (deref to connection) to query execution:

```rust
let mut tx = pool.begin().await?;

sqlx::query!("INSERT INTO users (name, email) VALUES ($1, $2)", name, email)
    .execute(&mut *tx)
    .await?;

sqlx::query!("INSERT INTO audit_log (action) VALUES ($1)", "user_created")
    .execute(&mut *tx)
    .await?;

tx.commit().await?;
```

## Commit and Rollback

```rust
let mut tx = pool.begin().await?;

match do_work(&mut tx).await {
    Ok(_) => tx.commit().await?,
    Err(e) => {
        tx.rollback().await?;
        return Err(e);
    }
}
```

## Auto-Rollback on Drop

If a transaction is dropped without calling `commit()` or `rollback()`, it is **automatically rolled back**. This makes the `?` operator safe:

```rust
async fn create_user(pool: &PgPool, name: &str) -> Result<User, sqlx::Error> {
    let mut tx = pool.begin().await?;

    let user = sqlx::query_as!(User,
        "INSERT INTO users (name) VALUES ($1) RETURNING *", name
    )
    .fetch_one(&mut *tx)
    .await?; // if this fails, tx is dropped → auto rollback

    sqlx::query!("INSERT INTO profiles (user_id) VALUES ($1)", user.id)
        .execute(&mut *tx)
        .await?; // if this fails, tx is dropped → auto rollback

    tx.commit().await?;
    Ok(user)
}
```

## Nested Transactions (Savepoints)

Calling `begin()` on a transaction creates a savepoint:

```rust
let mut tx = pool.begin().await?;

// outer work
sqlx::query!("INSERT INTO orders (user_id) VALUES ($1)", user_id)
    .execute(&mut *tx)
    .await?;

// nested savepoint
let mut savepoint = tx.begin().await?;
match process_payment(&mut savepoint).await {
    Ok(_) => savepoint.commit().await?,
    Err(_) => {
        savepoint.rollback().await?;
        // outer transaction still valid — order is inserted
        // can try alternative payment method
    }
}

tx.commit().await?;
```

## Passing Transactions to Functions

Use `&mut Transaction` or the generic `Executor` trait:

### Concrete Type

```rust
async fn insert_user(
    tx: &mut sqlx::Transaction<'_, sqlx::Postgres>,
    name: &str,
) -> Result<i64, sqlx::Error> {
    let id = sqlx::query_scalar!(
        "INSERT INTO users (name) VALUES ($1) RETURNING id", name
    )
    .fetch_one(&mut **tx)
    .await?;
    Ok(id)
}
```

### Generic Executor (Accepts Pool or Transaction)

```rust
async fn get_user<'e, E>(executor: E, id: i64) -> Result<User, sqlx::Error>
where
    E: sqlx::Executor<'e, Database = sqlx::Postgres>,
{
    sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(executor)
        .await
}

// Works with both:
let user = get_user(&pool, 1).await?;
let user = get_user(&mut *tx, 1).await?;
```

## Isolation Levels (PostgreSQL)

```rust
// Read Committed (default)
let mut tx = pool.begin().await?;

// Serializable
let mut tx = pool.begin_with("BEGIN ISOLATION LEVEL SERIALIZABLE").await?;

// Repeatable Read
let mut tx = pool.begin_with("BEGIN ISOLATION LEVEL REPEATABLE READ").await?;

// Read Uncommitted (treated as Read Committed in Postgres)
let mut tx = pool.begin_with("BEGIN ISOLATION LEVEL READ UNCOMMITTED").await?;
```

## Type Aliases

| Alias | Full Type |
|-------|-----------|
| `PgTransaction<'c>` | `Transaction<'c, Postgres>` |
| `MySqlTransaction<'c>` | `Transaction<'c, MySql>` |
| `SqliteTransaction<'c>` | `Transaction<'c, Sqlite>` |

## Common Pitfalls

- **Forgetting `&mut *tx`**: Must dereference when passing to query methods
- **Holding transactions too long**: Blocks other operations; keep transactions short
- **Ignoring commit errors**: `commit().await?` can fail (network, constraint violations)
- **Serialization failures**: Serializable transactions may need retry logic
