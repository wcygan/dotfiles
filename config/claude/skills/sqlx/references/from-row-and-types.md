---
title: FromRow & Type Mappings
description: FromRow derive macro, field attributes, PostgreSQL/MySQL/SQLite type mapping tables, custom types, Encode/Decode
tags: [sqlx, fromrow, types, derive, postgres, mysql, sqlite, encode, decode]
---

# FromRow & Type Mappings

## FromRow Derive

Maps database rows to Rust structs automatically:

```rust
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    email: String,
    created_at: chrono::NaiveDateTime,
}
```

## Field Attributes

### `#[sqlx(rename = "...")]`

Map struct field to differently-named column:

```rust
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    #[sqlx(rename = "user_name")]
    name: String,
}
```

### `#[sqlx(rename_all = "...")]`

Struct-level case transformation:

```rust
#[derive(sqlx::FromRow)]
#[sqlx(rename_all = "camelCase")]
struct User {
    user_id: i64,      // maps to "userId"
    first_name: String, // maps to "firstName"
}
```

Options: `camelCase`, `snake_case`, `PascalCase`, `SCREAMING_SNAKE_CASE`, `kebab-case`, `lowercase`, `UPPERCASE`

### `#[sqlx(default)]`

Use `Default::default()` for missing columns:

```rust
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    #[sqlx(default)]
    bio: String, // defaults to "" if column missing
}

// Or at struct level (requires Default impl)
#[derive(sqlx::FromRow, Default)]
#[sqlx(default)]
struct Config {
    timeout: i32,
    retries: i32,
}
```

### `#[sqlx(flatten)]`

Compose nested structs:

```rust
#[derive(sqlx::FromRow)]
struct Address {
    street: String,
    city: String,
}

#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    #[sqlx(flatten)]
    address: Address, // street and city columns extracted from same row
}
```

### `#[sqlx(skip)]`

Skip field, use `Default::default()`:

```rust
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    #[sqlx(skip)]
    cached_display: String, // not from database
}
```

### `#[sqlx(try_from = "...")]`

Convert database type via `TryFrom`:

```rust
#[derive(sqlx::FromRow)]
struct Record {
    #[sqlx(try_from = "i64")]
    id: u64, // MySQL returns i64, convert to u64
}
```

### `#[sqlx(json)]`

Deserialize JSON columns via serde:

```rust
#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    #[sqlx(json)]
    preferences: UserPreferences, // stored as JSON/JSONB
}
```

## PostgreSQL Type Mappings

### Standard Types

| Rust Type | PostgreSQL Type |
|-----------|-----------------|
| `bool` | BOOL |
| `i16` | SMALLINT, INT2 |
| `i32` | INT, INT4, SERIAL |
| `i64` | BIGINT, INT8, BIGSERIAL |
| `f32` | REAL, FLOAT4 |
| `f64` | DOUBLE PRECISION, FLOAT8 |
| `String` / `&str` | VARCHAR, TEXT, CHAR(N), NAME, CITEXT |
| `Vec<u8>` / `&[u8]` | BYTEA |

### Date/Time (feature: `chrono`)

| Rust Type | PostgreSQL Type |
|-----------|-----------------|
| `chrono::NaiveDateTime` | TIMESTAMP |
| `chrono::DateTime<Utc>` | TIMESTAMPTZ |
| `chrono::NaiveDate` | DATE |
| `chrono::NaiveTime` | TIME |

### Date/Time (feature: `time`)

| Rust Type | PostgreSQL Type |
|-----------|-----------------|
| `time::PrimitiveDateTime` | TIMESTAMP |
| `time::OffsetDateTime` | TIMESTAMPTZ |
| `time::Date` | DATE |
| `time::Time` | TIME |

### Extended Types

| Rust Type | PostgreSQL Type | Feature |
|-----------|-----------------|---------|
| `uuid::Uuid` | UUID | `uuid` |
| `serde_json::Value` | JSON, JSONB | `json` |
| `rust_decimal::Decimal` | NUMERIC | `rust_decimal` |
| `bigdecimal::BigDecimal` | NUMERIC | `bigdecimal` |
| `ipnetwork::IpNetwork` | INET, CIDR | `ipnetwork` |
| `mac_address::MacAddress` | MACADDR | `mac_address` |
| `bit_vec::BitVec` | BIT, VARBIT | `bit-vec` |

### Collections and Composite

| Rust Type | PostgreSQL Type |
|-----------|-----------------|
| `Vec<T>` | `T[]` (arrays) |
| `PgRange<T>` | INT4RANGE, TSRANGE, etc. |
| `PgInterval` | INTERVAL |
| `PgMoney` | MONEY |

## Custom Enums

### String-Variant Enum

```rust
#[derive(sqlx::Type)]
#[sqlx(type_name = "user_role", rename_all = "lowercase")]
enum UserRole {
    Admin,
    User,
    Guest,
}
```

Requires matching PostgreSQL enum:
```sql
CREATE TYPE user_role AS ENUM ('admin', 'user', 'guest');
```

### Integer-Repr Enum

```rust
#[derive(sqlx::Type)]
#[repr(i32)]
enum Status {
    Active = 1,
    Inactive = 0,
    Suspended = -1,
}
```

## Custom Newtype Wrapper

```rust
#[derive(sqlx::Type)]
#[sqlx(transparent)]
struct UserId(i64);
```

This delegates Encode/Decode to the inner type.

## MySQL Type Differences

| Rust Type | MySQL Type |
|-----------|------------|
| `u8` | TINYINT UNSIGNED |
| `u16` | SMALLINT UNSIGNED |
| `u32` | INT UNSIGNED |
| `u64` | BIGINT UNSIGNED |
| `chrono::NaiveDateTime` | DATETIME |
| `chrono::DateTime<Utc>` | TIMESTAMP |

## SQLite Type Differences

SQLite uses affinity-based typing:

| Rust Type | SQLite Affinity |
|-----------|-----------------|
| `bool` | BOOLEAN (stored as INTEGER) |
| `i32` / `i64` | INTEGER |
| `f64` | REAL |
| `String` | TEXT |
| `Vec<u8>` | BLOB |
