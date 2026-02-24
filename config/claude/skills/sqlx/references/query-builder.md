---
title: QueryBuilder
description: Dynamic SQL construction — push, push_bind, separated lists, bulk inserts, SQL injection prevention, bind parameter limits
tags: [sqlx, querybuilder, dynamic, sql injection, bulk insert, separated]
---

# QueryBuilder

Runtime SQL construction for dynamic queries. Use when the query structure depends on runtime conditions.

## When to Use QueryBuilder vs Macros

| Scenario | Use |
|----------|-----|
| Static query, known at compile time | `query!` / `query_as!` |
| Dynamic WHERE clauses | `QueryBuilder` |
| Dynamic column selection | `QueryBuilder` |
| Bulk INSERT with variable row count | `QueryBuilder` |
| IN clause with variable-length list | `QueryBuilder` |

## Basic Usage

```rust
use sqlx::QueryBuilder;
use sqlx::Postgres; // or MySql, Sqlite

let mut qb: QueryBuilder<Postgres> = QueryBuilder::new("SELECT * FROM users WHERE 1=1");

if let Some(name) = filter_name {
    qb.push(" AND name = ").push_bind(name);
}

if let Some(age) = filter_min_age {
    qb.push(" AND age >= ").push_bind(age);
}

qb.push(" ORDER BY created_at DESC LIMIT ").push_bind(limit);

let users = qb.build_query_as::<User>()
    .fetch_all(&pool)
    .await?;
```

## Core Methods

### push() — Append Raw SQL

```rust
qb.push("SELECT * FROM users");
qb.push(" WHERE active = true");
```

**WARNING**: Never use `push()` with user input. It inserts SQL directly — vulnerable to injection.

### push_bind() — Safe Parameter Binding

```rust
qb.push(" WHERE email = ").push_bind(user_email);
// PostgreSQL: WHERE email = $1
// MySQL:      WHERE email = ?
```

Always use `push_bind()` for any value that originates from user input.

### separated() — Build Lists

```rust
let mut qb: QueryBuilder<Postgres> = QueryBuilder::new("SELECT * FROM users WHERE id IN (");
let mut sep = qb.separated(", ");

for id in &user_ids {
    sep.push_bind(*id);
}

sep.push_unseparated(")");

let users = qb.build_query_as::<User>()
    .fetch_all(&pool)
    .await?;
```

### push_values() — Bulk INSERT

```rust
let mut qb: QueryBuilder<Postgres> = QueryBuilder::new(
    "INSERT INTO users (name, email) "
);

qb.push_values(users.iter(), |mut b, user| {
    b.push_bind(&user.name)
     .push_bind(&user.email);
});

qb.build().execute(&pool).await?;
```

Generates: `INSERT INTO users (name, email) VALUES ($1, $2), ($3, $4), ...`

### push_tuples() — Tuple WHERE Clauses

```rust
let mut qb: QueryBuilder<Postgres> = QueryBuilder::new(
    "SELECT * FROM items WHERE (category, id) IN "
);

qb.push_tuples(items.iter(), |mut b, item| {
    b.push_bind(&item.category)
     .push_bind(item.id);
});
```

Generates: `WHERE (category, id) IN (($1, $2), ($3, $4), ...)`

## Building the Final Query

```rust
// Untyped (returns rows)
let query = qb.build();
let rows = query.fetch_all(&pool).await?;

// Typed via FromRow
let query = qb.build_query_as::<User>();
let users = query.fetch_all(&pool).await?;

// Single scalar column
let query = qb.build_query_scalar::<i64>();
let ids = query.fetch_all(&pool).await?;
```

## Bind Parameter Limits

Databases have maximum bind parameter counts:

| Database | Max Bind Parameters |
|----------|---------------------|
| PostgreSQL | 65,535 |
| MySQL | 65,535 |
| SQLite | 32,766 |

For bulk inserts, chunk your data:

```rust
const BIND_LIMIT: usize = 65535;
let columns_per_row = 3;

for chunk in users.chunks(BIND_LIMIT / columns_per_row) {
    let mut qb: QueryBuilder<Postgres> = QueryBuilder::new(
        "INSERT INTO users (name, email, role) "
    );

    qb.push_values(chunk, |mut b, user| {
        b.push_bind(&user.name)
         .push_bind(&user.email)
         .push_bind(&user.role);
    });

    qb.build().execute(&pool).await?;
}
```

## PostgreSQL UNNEST Alternative

For large Postgres bulk inserts, `UNNEST` is more efficient than large VALUES:

```rust
let names: Vec<&str> = users.iter().map(|u| u.name.as_str()).collect();
let emails: Vec<&str> = users.iter().map(|u| u.email.as_str()).collect();

sqlx::query!(
    "INSERT INTO users (name, email)
     SELECT * FROM UNNEST($1::text[], $2::text[])",
    &names,
    &emails,
)
.execute(&pool)
.await?;
```

Benefits: single bind parameter per column (not per row), no bind limit issues.

## SQL Injection Prevention Checklist

- `push()` — **UNSAFE** for user input. Only use for static SQL fragments.
- `push_bind()` — **SAFE**. Always use for user-provided values.
- `separated().push_bind()` — **SAFE**. Bind parameters in lists.
- `push_values()` — **SAFE**. Binds each value as a parameter.
- Column/table names — Cannot be parameterized. Validate against an allowlist:

```rust
let allowed_columns = ["name", "email", "created_at"];
let order_by = if allowed_columns.contains(&user_input_column.as_str()) {
    user_input_column
} else {
    return Err(anyhow!("Invalid column"));
};
qb.push(&format!(" ORDER BY {order_by}"));
```

## Resetting for Reuse

```rust
let mut qb: QueryBuilder<Postgres> = QueryBuilder::new("INSERT INTO logs (msg) VALUES (");

for msg in messages {
    qb.push_bind(msg);
    qb.push(")");
    qb.build().execute(&pool).await?;
    qb.reset(); // back to initial state
    qb.push_bind(""); // re-prep for next iteration — but typically just create a new builder
}
```

In practice, creating a new `QueryBuilder` per iteration is clearer.
