---
title: Migrations
description: SQLx migration system — migrate! macro, sqlx-cli, file naming conventions, reversible migrations, embedded migrations, programmatic execution
tags: [sqlx, migration, migrate, sqlx-cli, schema, database]
---

# Migrations

## Overview

SQLx provides two migration approaches:
1. **sqlx-cli**: Command-line tool for creating and running migrations
2. **migrate! macro**: Embeds migrations into the binary for programmatic execution

Requires the `migrate` feature in Cargo.toml.

## sqlx-cli Setup

```bash
# Install with your database
cargo install sqlx-cli --features postgres
# or
cargo install sqlx-cli --features mysql,sqlite
```

## File Naming Convention

Migrations live in a `migrations/` directory at project root:

```
migrations/
├── 20240101000000_create_users.sql
├── 20240102000000_create_posts.sql
└── 20240103000000_add_email_to_users.sql
```

Format: `<VERSION>_<DESCRIPTION>.sql`
- Version: `i64` > 0, typically a timestamp (YYYYMMDDHHmmss)
- Description: snake_case, describes the change

## Creating Migrations

```bash
# Creates timestamped file in migrations/
sqlx migrate add create_users

# Creates reversible migration (up + down files)
sqlx migrate add -r create_users
```

### Simple (Forward-Only)

`migrations/20240101000000_create_users.sql`:
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Reversible (Up + Down)

`migrations/20240101000000_create_users.up.sql`:
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

`migrations/20240101000000_create_users.down.sql`:
```sql
DROP TABLE users;
```

## Running Migrations via CLI

```bash
# Run all pending migrations
sqlx migrate run

# Revert the last migration (reversible only)
sqlx migrate revert

# Show migration status
sqlx migrate info

# Run against specific database
DATABASE_URL=postgres://user:pass@localhost/db sqlx migrate run
```

## Embedded Migrations (migrate! Macro)

Embeds migrations into the binary:

```rust
use sqlx::migrate::Migrator;

// Loads from ./migrations/ relative to CARGO_MANIFEST_DIR
static MIGRATOR: Migrator = sqlx::migrate!();

// Or custom path
static MIGRATOR: Migrator = sqlx::migrate!("db/migrations");
```

### Running at Startup

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect("postgres://...")
        .await?;

    // Run embedded migrations
    sqlx::migrate!().run(&pool).await?;

    // Start application...
    Ok(())
}
```

### Programmatic Control

```rust
let migrator = sqlx::migrate!();

// Run all pending
migrator.run(&pool).await?;

// Undo last migration
migrator.undo(&pool, 1).await?;

// Check if migrations are current
migrator.ensure_current(&pool).await?;
```

## Migration Table

SQLx tracks applied migrations in `_sqlx_migrations`:

| Column | Type | Purpose |
|--------|------|---------|
| version | BIGINT | Migration version number |
| description | TEXT | Migration description |
| installed_on | TIMESTAMPTZ | When migration was applied |
| success | BOOLEAN | Whether it completed successfully |
| checksum | BYTEA | SHA-384 hash of migration SQL |
| execution_time | BIGINT | Time taken in nanoseconds |

## Best Practices

### Migration Content

- **One logical change per migration**: Don't combine table creation with data migration
- **Always test down migrations**: Verify they cleanly reverse the up migration
- **Use transactions**: PostgreSQL DDL is transactional; wrap in BEGIN/COMMIT for atomicity
- **Avoid data-dependent migrations**: Keep schema changes separate from data migrations

### Naming

```bash
# Good: descriptive, specific
sqlx migrate add create_users_table
sqlx migrate add add_email_index_to_users
sqlx migrate add create_order_items_with_fk

# Bad: vague, ambiguous
sqlx migrate add update
sqlx migrate add fix
sqlx migrate add changes
```

### Production Deployment

```rust
// Run migrations before starting the web server
async fn main() -> Result<()> {
    let pool = create_pool().await?;

    // Migrations run in a transaction; safe for concurrent deploys
    sqlx::migrate!().run(&pool).await?;

    start_server(pool).await
}
```

## Common Pitfalls

- **Editing applied migrations**: Checksum mismatch will cause errors; create a new migration instead
- **Missing `migrate` feature**: The macro requires `features = ["migrate"]` in Cargo.toml
- **Concurrent migration runs**: SQLx uses advisory locks to prevent conflicts, but verify your setup
- **Large data migrations**: Run as separate scripts, not embedded migrations (avoid blocking startup)
