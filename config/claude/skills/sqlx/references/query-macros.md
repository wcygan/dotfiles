---
title: Query Macros
description: Compile-time checked SQL query macros — query!, query_as!, query_scalar!, query_file!, offline mode, bind parameters, type overrides, nullability
tags: [sqlx, query, macro, compile-time, bind, nullability, offline]
---

# Query Macros

## Macro Variants

| Macro | Output | Use Case |
|-------|--------|----------|
| `query!` | Anonymous struct | Quick queries, ad-hoc results |
| `query_as!` | Named struct | Typed results via explicit struct |
| `query_scalar!` | Single value | Extract one column |
| `query_file!` | Anonymous struct | SQL in separate `.sql` file |
| `query_file_as!` | Named struct | `.sql` file + explicit struct |
| `query_unchecked!` | Anonymous struct | Skip type checking (syntax only) |

## Compile-Time Database Connection

The macros introspect your database schema at compile time:

- Set `DATABASE_URL` env var pointing to a running database
- Or place it in `.env` at project root (uses `dotenvy` crate)
- Schema must match what the query expects
- Database URL scheme (`postgres://`, `mysql://`, `sqlite://`) determines backend

```bash
# .env file
DATABASE_URL=postgres://user:pass@localhost:5432/mydb
```

## Bind Parameters

Database-specific placeholder syntax:

- **PostgreSQL**: `$1`, `$2`, ... (1-based positional)
- **MySQL/SQLite**: `?` (matches arguments in order)

```rust
// PostgreSQL
let user = sqlx::query!("SELECT * FROM users WHERE id = $1 AND active = $2", user_id, true)
    .fetch_one(&pool)
    .await?;

// MySQL / SQLite
let user = sqlx::query!("SELECT * FROM users WHERE id = ? AND active = ?", user_id, true)
    .fetch_one(&pool)
    .await?;
```

Both `T` and `Option<T>` are accepted. `None` binds as `NULL`.

## Fetching Results

| Expected Rows | Method | Returns |
|---------------|--------|---------|
| None (INSERT/UPDATE/DELETE) | `.execute(&pool).await` | `Result<QueryResult>` |
| Zero or one | `.fetch_optional(&pool).await` | `Result<Option<Row>>` |
| Exactly one | `.fetch_one(&pool).await` | `Result<Row>` |
| Stream | `.fetch(&pool)` | `impl Stream<Item = Result<Row>>` |
| All rows | `.fetch_all(&pool).await` | `Result<Vec<Row>>` |

All methods accept `&Pool`, `&mut Connection`, or `&mut Transaction`.

## Nullability Handling

The macro infers nullability from database constraints (`NOT NULL`).

### Override Syntax (PostgreSQL/SQLite)

```rust
// Force non-null (panic if NULL returned)
sqlx::query!(r#"SELECT id as "id!" FROM users"#)

// Force nullable
sqlx::query!(r#"SELECT id as "id?" FROM users"#)

// Override type
sqlx::query!(r#"SELECT id as "id: uuid::Uuid" FROM users"#)

// Combined: non-null + custom type
sqlx::query!(r#"SELECT id as "id!: uuid::Uuid" FROM users"#)
```

### MySQL Override Syntax

```rust
// MySQL uses backtick syntax
sqlx::query!("SELECT id as `id!` FROM users")
```

### When to Override

- Outer JOINs: macro may infer nullable when you know it won't be
- Computed columns: type inference may be wrong
- COALESCE/IFNULL: macro may not detect guaranteed non-null

## query_as! — Named Struct Output

```rust
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    email: String,
}

let users = sqlx::query_as!(User, "SELECT id, name, email FROM users")
    .fetch_all(&pool)
    .await?;
```

## query_scalar! — Single Column

```rust
let count = sqlx::query_scalar!("SELECT COUNT(*) FROM users")
    .fetch_one(&pool)
    .await?;

let ids: Vec<i64> = sqlx::query_scalar!("SELECT id FROM users WHERE active = true")
    .fetch_all(&pool)
    .await?;
```

## query_file! — External SQL Files

```rust
// Loads from ./sql/get_user.sql relative to CARGO_MANIFEST_DIR
let user = sqlx::query_file!("sql/get_user.sql", user_id)
    .fetch_one(&pool)
    .await?;

// With named struct
let user = sqlx::query_file_as!(User, "sql/get_user.sql", user_id)
    .fetch_one(&pool)
    .await?;
```

## Offline Mode (CI/CD)

For environments without database access at compile time:

```bash
# 1. With database running, prepare cached query metadata
cargo sqlx prepare

# 2. Commit the generated .sqlx/ directory

# 3. In CI, build without DATABASE_URL — macro uses cached metadata
cargo build

# 4. Verify cache is current
cargo sqlx prepare --check
```

The `.sqlx/` directory contains JSON files with query metadata. Add it to version control.

## Runtime query() (Non-Macro)

For queries that don't need compile-time checking:

```rust
let rows = sqlx::query("SELECT * FROM users WHERE id = $1")
    .bind(user_id)
    .fetch_all(&pool)
    .await?;

// With typed output
let users = sqlx::query_as::<_, User>("SELECT id, name, email FROM users")
    .fetch_all(&pool)
    .await?;
```

## Common Pitfalls

- **Forgetting `r#"..."#`**: Required when using `"column!"` override syntax (inner quotes)
- **Wrong placeholder style**: `$1` for Postgres, `?` for MySQL/SQLite
- **Stale .sqlx cache**: Run `cargo sqlx prepare` after schema changes
- **Missing DATABASE_URL**: Macro won't compile without it or `.sqlx/` cache
- **Column count mismatch**: `query_as!` requires SELECT columns to match struct fields exactly
