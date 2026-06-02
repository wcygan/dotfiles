---
title: TiDB Flashback (Recover from Drops/Truncates)
---

# TiDB Flashback (Recover from Drops/Truncates)

Use flashback to recover from accidental `DROP` / `TRUNCATE` if you catch it before GC permanently removes the historical versions.

Important: Flashback is constrained by GC. Default `tidb_gc_life_time` is often short (for example, 10 minutes). Act quickly.

## Before you try to recover

1. Confirm you are on TiDB (not MySQL): `SELECT VERSION();`
2. Check the GC safe point:

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

If the drop/truncate happened before the safe point, flashback cannot recover it.

## FLASHBACK TABLE (TiDB v4.0+)

Recover a dropped table:

```sql
FLASHBACK TABLE t;
```

Recover a truncated table:

- After `TRUNCATE`, the table name still exists, so you must recover to a new name:

```sql
FLASHBACK TABLE t TO t_recovered;
```

Notes:

- You cannot restore the same deleted table multiple times (the restored table reuses the same table ID).

## FLASHBACK DATABASE (TiDB v6.4.0+)

Recover a dropped database:

```sql
FLASHBACK DATABASE test;
```

Recover and rename:

```sql
FLASHBACK DATABASE test TO test_recovered;
```

Notes:

- You cannot restore the same database multiple times (schema IDs must be globally unique).

## FLASHBACK CLUSTER TO TIMESTAMP / TSO (high impact)

Use this to restore the whole cluster to a specific point in time.

Availability / safety gates:

- Some restricted or managed deployments may not expose this operation.
- Requires `SUPER` privilege.
- Must be within GC lifetime.
- Do not specify a future timestamp/TSO.
- During execution, TiDB disconnects related connections and blocks reads/writes. It cannot be canceled once started.
- It writes old data forward with a new timestamp (it does not delete current data). Ensure enough storage space.
- If you use TiCDC, metadata rollbacks are not replicated; plan to pause changefeeds and reconcile schemas after.

Syntax:

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
FLASHBACK CLUSTER TO TSO 445494839813079041;
```

Get a TSO for a precise point:

```sql
SELECT @@tidb_current_ts;
```
