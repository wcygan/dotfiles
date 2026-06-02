---
title: TiDB AUTO_RANDOM (SQL)
---

# TiDB AUTO_RANDOM (SQL)

`AUTO_RANDOM` is used to avoid write hotspots that can happen with sequential keys in distributed storage.

## When to prefer AUTO_RANDOM

- When you would otherwise use `BIGINT AUTO_INCREMENT` as the primary key in a write-heavy workload.
- When you do not require strictly increasing IDs.

## DDL patterns

Valid forms (must be `BIGINT` and part of the primary key; typically first PK column):

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
```

Insert behavior:

- If you omit the `AUTO_RANDOM` column in `INSERT`, TiDB generates a random unique value.
- If you specify it explicitly, TiDB inserts it as provided (but this is usually discouraged).

## Operational gotchas

- Explicit inserts can require enabling `@@allow_auto_random_explicit_insert = 1`.
- After explicit inserts in multi-node setups, you might need to "rebase" to avoid collisions:

```sql
ALTER TABLE t AUTO_RANDOM_BASE = 0;
```

## Restrictions to remember

- You cannot add/remove/modify the `AUTO_RANDOM` attribute later with `ALTER TABLE`.
- You cannot combine `AUTO_RANDOM` with `AUTO_INCREMENT` or `DEFAULT` on the same column.
