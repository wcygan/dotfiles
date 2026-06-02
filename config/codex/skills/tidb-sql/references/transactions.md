---
title: TiDB Transactions (Optimistic vs Pessimistic)
---

# TiDB Transactions (Optimistic vs Pessimistic)

TiDB supports both pessimistic and optimistic transaction modes.
MySQL/InnoDB users typically expect pessimistic behavior by default.

## Choose a mode

- Prefer **pessimistic** when conflicts are common or when the application cannot safely retry on commit failures.
- Consider **optimistic** when write-write conflicts are rare and you can handle commit failures in the app.

## Set default mode (cluster-wide)

```sql
SET GLOBAL tidb_txn_mode = 'pessimistic';
-- or:
SET GLOBAL tidb_txn_mode = 'optimistic';
```

## Force mode per transaction

```sql
BEGIN PESSIMISTIC;
-- ... DML ...
COMMIT;
```

```sql
BEGIN OPTIMISTIC;
-- ... DML ...
COMMIT;
```

## App-level rule (optimistic)

If you generate SQL intended for optimistic transactions, require the caller/application to handle `COMMIT` errors and retry the whole transaction safely (idempotency + retry loop).

