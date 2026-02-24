---
name: sqlx
description: SQLx Rust async SQL toolkit expert. Assists with compile-time checked queries, connection pooling, migrations, transactions, FromRow derive, QueryBuilder, type mappings, and testing. Use when working with SQLx, database queries in Rust, sqlx::query!, Pool configuration, database migrations, or Rust database code. Keywords: sqlx, rust database, query macro, pool, migration, transaction, FromRow, postgres rust, mysql rust, sqlite rust, compile-time SQL
---

# SQLx Expert

Comprehensive assistant for the SQLx async SQL toolkit in Rust. Covers compile-time checked queries, connection pooling, migrations, transactions, type mappings, dynamic query building, error handling, and testing.

## Supported Databases

- **PostgreSQL** (`sqlx-postgres`)
- **MySQL** (`sqlx-mysql`)
- **SQLite** (`sqlx-sqlite`)

## When Activated

### Analysis Mode
- Review SQLx code for correctness, idiomatic patterns, and SQL injection risks
- Check query macro usage (proper bind parameters, type overrides, nullability)
- Audit pool configuration (connection limits, timeouts, lifecycle)
- Validate migration ordering and reversibility
- Verify FromRow derive attributes and type mappings

### Generation Mode
- Write compile-time checked queries with `query!` / `query_as!`
- Set up connection pools with appropriate `PoolOptions`
- Create migration files with proper naming conventions
- Implement transaction patterns with error handling
- Build dynamic queries safely with `QueryBuilder`
- Generate `#[sqlx::test]` test functions with fixtures

## Key Patterns

### Compile-Time Query Checking
- Requires `DATABASE_URL` at compile time (or offline mode with `.sqlx/` directory)
- Use `cargo sqlx prepare` for CI without database access
- Nullability inferred from schema; override with `"column!"` or `"column?"`

### Connection Pool
- Always configure `max_connections`, `acquire_timeout`, and `idle_timeout`
- Use `connect_lazy` when connection isn't needed immediately
- Clone is cheap (reference-counted handle)
- Call `pool.close().await` for graceful shutdown

### Transactions
- Auto-rollback on drop if not committed
- Use `&mut *tx` when passing to query execution
- Nested transactions become savepoints

### SQL Injection Prevention
- Never use `push()` with user input in `QueryBuilder`
- Always use `push_bind()` for untrusted values
- `query!` macro bind parameters are inherently safe

### Feature Flags
- Runtime: `runtime-tokio` or `runtime-async-std`
- TLS: `tls-rustls` (preferred) or `tls-native-tls`
- Types: `chrono`, `time`, `uuid`, `rust_decimal`, `bigdecimal`, `json`, `ipnetwork`
- Testing: `migrate` feature required for `#[sqlx::test]`

## Reference Files

Detailed guidance on specific topics:

- **Query macros** — `query!`, `query_as!`, `query_scalar!`, offline mode, bind params, type overrides

  References: [query-macros](references/query-macros.md)

- **Connection pooling** — Pool creation, PoolOptions, configuration, lifecycle, Executor impl

  References: [connection-pooling](references/connection-pooling.md)

- **FromRow & type mappings** — derive attributes, Postgres/MySQL/SQLite type tables, custom types

  References: [from-row-and-types](references/from-row-and-types.md)

- **Transactions** — begin/commit/rollback, savepoints, auto-rollback, isolation levels

  References: [transactions](references/transactions.md)

- **Migrations** — migrate! macro, sqlx-cli, file naming, reversible migrations, programmatic execution

  References: [migrations](references/migrations.md)

- **QueryBuilder** — dynamic SQL, push_bind, separated lists, bulk inserts, SQL injection safety

  References: [query-builder](references/query-builder.md)

- **Testing** — #[sqlx::test], fixtures, test database management, Pool/PoolConnection signatures

  References: [testing](references/testing.md)

- **Error handling** — Error enum variants, DatabaseError matching, common error patterns

  References: [error-handling](references/error-handling.md)

## Cargo.toml Setup

Typical feature configuration:

```toml
[dependencies]
sqlx = { version = "0.8", features = [
    "runtime-tokio",
    "tls-rustls",
    "postgres",        # or "mysql", "sqlite"
    "migrate",
    "chrono",          # or "time"
    "uuid",
    "json",
] }
```

## Common sqlx-cli Commands

```bash
# Install CLI
cargo install sqlx-cli --features postgres

# Create database
sqlx database create

# Create migration
sqlx migrate add <name>

# Run migrations
sqlx migrate run

# Prepare offline query data
cargo sqlx prepare

# Verify offline data is current
cargo sqlx prepare --check
```
